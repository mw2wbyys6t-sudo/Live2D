#!/usr/bin/env python3
"""
Live2D Master Agent - 工作流引擎
实现工作流模式，支持步骤编排、重试、回滚
"""

import time
import traceback
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field

from .interfaces import WorkflowStep


@dataclass
class WorkflowContext:
    """工作流上下文"""
    data: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)
    
    def set(self, key: str, value):
        self.data[key] = value
    
    def add_error(self, error: str):
        self.errors.append(error)


@dataclass
class StepResult:
    """步骤执行结果"""
    success: bool
    context: WorkflowContext
    execution_time: float
    retry_count: int = 0
    error: Optional[str] = None


class WorkflowEngine:
    """
    工作流引擎
    
    特性:
    - 支持步骤顺序执行
    - 支持步骤重试
    - 支持错误处理
    - 支持执行时间统计
    """
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.steps: List[WorkflowStep] = []
        self.on_step_complete: Optional[Callable] = None
        self.on_step_error: Optional[Callable] = None
    
    def add_step(self, step: WorkflowStep) -> 'WorkflowEngine':
        """添加步骤（支持链式调用）"""
        self.steps.append(step)
        return self
    
    def execute(self, initial_context: Optional[Dict] = None) -> WorkflowContext:
        """
        执行工作流
        
        Args:
            initial_context: 初始上下文数据
        
        Returns:
            执行后的上下文
        """
        context = WorkflowContext(data=initial_context or {})
        context.metadata['workflow_name'] = self.name
        context.metadata['start_time'] = time.time()
        
        print(f"\n{'='*60}")
        print(f"🚀 启动工作流: {self.name}")
        print(f"{'='*60}")
        
        for i, step in enumerate(self.steps, 1):
            result = self._execute_step(step, context, i)
            
            if not result.success:
                print(f"\n❌ 工作流失败于步骤 {i}: {step.get_name()}")
                if result.error:
                    print(f"   错误: {result.error}")
                break
            
            context = result.context
            
            # 回调通知
            if self.on_step_complete:
                self.on_step_complete(step, result)
        
        context.metadata['end_time'] = time.time()
        context.metadata['duration'] = (
            context.metadata['end_time'] - context.metadata['start_time']
        )
        
        print(f"\n{'='*60}")
        print(f"✅ 工作流完成")
        print(f"   耗时: {context.metadata['duration']:.2f}秒")
        print(f"{'='*60}\n")
        
        return context
    
    def _execute_step(
        self,
        step: WorkflowStep,
        context: WorkflowContext,
        step_number: int,
        max_retries: int = 3
    ) -> StepResult:
        """执行单个步骤（带重试）"""
        start_time = time.time()
        retry_count = 0
        last_error = None
        
        print(f"\n📍 步骤 {step_number}/{len(self.steps)}: {step.get_name()}")
        print(f"   {'─'*50}")
        
        while retry_count <= max_retries:
            try:
                if retry_count > 0:
                    print(f"   🔄 第 {retry_count} 次重试...")
                
                new_context = step.execute(context.data)
                
                # 更新上下文
                context.data.update(new_context)
                
                execution_time = time.time() - start_time
                print(f"   ✅ 完成 ({execution_time:.2f}s)")
                
                return StepResult(
                    success=True,
                    context=context,
                    execution_time=execution_time,
                    retry_count=retry_count
                )
                
            except Exception as e:
                retry_count += 1
                last_error = str(e)
                context.add_error(f"{step.get_name()}: {last_error}")
                
                if self.on_step_error:
                    self.on_step_error(step, e, retry_count)
                
                if not step.can_retry() or retry_count > max_retries:
                    break
                
                # 指数退避
                wait_time = 2 ** retry_count
                print(f"   ⚠️  失败: {last_error}")
                print(f"   ⏳ {wait_time}秒后重试...")
                time.sleep(wait_time)
        
        execution_time = time.time() - start_time
        print(f"   ❌ 最终失败 ({execution_time:.2f}s)")
        
        return StepResult(
            success=False,
            context=context,
            execution_time=execution_time,
            retry_count=retry_count,
            error=last_error
        )


class PipelineStep(WorkflowStep):
    """管道步骤基类"""
    
    def __init__(self, name: str, processor: Callable, can_retry: bool = True):
        self._name = name
        self._processor = processor
        self._can_retry = can_retry
    
    def execute(self, context: Dict) -> Dict:
        result = self._processor(context)
        if isinstance(result, dict):
            return result
        return context
    
    def get_name(self) -> str:
        return self._name
    
    def can_retry(self) -> bool:
        return self._can_retry
