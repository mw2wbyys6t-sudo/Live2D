#!/usr/bin/env python3
"""
Live2D Master Agent - 工作流引擎

编排工作流步骤，支持链式调用、自动重试和错误处理。
"""

import time
import logging
from typing import Dict, List, Optional

from core.interfaces import WorkflowStep

logger = logging.getLogger(__name__)


class WorkflowContext:
    """
    工作流上下文 - 传递步骤间的数据和状态

    提供字典式的数据存取，同时记录步骤执行历史。
    """

    def __init__(self, initial_data: Optional[Dict] = None):
        self._data = initial_data or {}
        self._history: List[Dict] = []

    def get(self, key: str, default=None):
        """获取上下文中的值"""
        return self._data.get(key, default)

    def set(self, key: str, value):
        """设置上下文中的值"""
        self._data[key] = value

    def update(self, data: Dict):
        """批量更新上下文"""
        self._data.update(data)

    def to_dict(self) -> Dict:
        """导出为字典"""
        return self._data.copy()

    def log_step(self, step_name: str, success: bool, message: str = ""):
        """记录步骤执行历史"""
        self._history.append({
            "step": step_name,
            "success": success,
            "message": message,
            "timestamp": time.time(),
        })

    def get_history(self) -> List[Dict]:
        """获取执行历史"""
        return self._history.copy()

    def __getitem__(self, key: str):
        return self._data[key]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data


class WorkflowEngine:
    """
    工作流引擎 - 编排和执行工作流步骤

    特性:
    - 链式添加步骤
    - 自动重试（指数退避）
    - 错误处理和上下文传递
    - 执行日志记录
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self._steps: List[WorkflowStep] = []
        self.steps: List[Dict] = []  # 兼容外部访问
        self._max_retries: int = 3
        self._retry_delay: float = 1.0  # 初始重试延迟（秒）
        self._execution_log: List[Dict] = []

    def add_step(self, step, name: Optional[str] = None) -> 'WorkflowEngine':
        """添加步骤（支持链式调用，兼容函数和WorkflowStep对象）"""
        if isinstance(step, WorkflowStep):
            self._steps.append(step)
        else:
            # 兼容普通函数
            self._steps.append(step)
            if name:
                self.steps.append({'func': step, 'name': name})
            else:
                self.steps.append({'func': step, 'name': getattr(step, '__name__', 'unknown')})
        return self

    def set_max_retries(self, max_retries: int) -> 'WorkflowEngine':
        """设置最大重试次数"""
        self._max_retries = max_retries
        return self

    def add_step(self, step_func, name: Optional[str] = None):
        """添加工作流步骤"""
        self.steps.append({
            'func': step_func,
            'name': name or step_func.__name__,
        })

    def execute(self, context: Optional[Dict] = None) -> Dict:
        """
        执行工作流

        Args:
            initial_context: 初始上下文

        Returns:
            最终上下文
        """
        context = initial_context or {}
        context['_engine'] = self.name
        context['_start_time'] = time.time()

        for step in self._steps:
            step_name = step.get_name()
            step_start = time.time()
            retries = 0
            success = False

            while retries <= (self._max_retries if step.can_retry() else 0):
                try:
                    context = step.execute(context)
                    success = True
                    break
                except Exception as e:
                    retries += 1
                    if retries <= self._max_retries and step.can_retry():
                        delay = self._retry_delay * (2 ** (retries - 1))
                        logger.warning(
                            f"步骤 '{step_name}' 执行失败 "
                            f"(第{retries}次重试，{delay:.1f}秒后重试): {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"步骤 '{step_name}' 执行失败，已达最大重试次数: {e}")
                        context['_error'] = str(e)
                        context['_failed_step'] = step_name
                        break

            step_duration = time.time() - step_start
            self._execution_log.append({
                'step': step_name,
                'success': success,
                'retries': retries,
                'duration': round(step_duration, 3),
            })

            if not success:
                break

        context['_end_time'] = time.time()
        context['_duration'] = round(context['_end_time'] - context['_start_time'], 3)
        context['_execution_log'] = self._execution_log

        return context

    def get_execution_log(self) -> List[Dict]:
        """获取执行日志"""
        return self._execution_log.copy()

    def reset(self) -> 'WorkflowEngine':
        """重置引擎状态"""
        self._steps.clear()
        self._execution_log.clear()
        return self
