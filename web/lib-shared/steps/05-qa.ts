import type { QAIssue, QAReport, PsdLayerPlan } from '../types';

export interface QAStepInput {
  plan: PsdLayerPlan;
  strictMode?: boolean;
}

export interface QAStepOutput {
  report: QAReport;
  passed: boolean;
}

export class QAStep {
  async execute(input: QAStepInput): Promise<QAStepOutput> {
    const issues: QAIssue[] = [];
    
    if (!input.plan.layers.find(l => l.name.toLowerCase().includes('face'))) {
      issues.push({
        severity: 'warning',
        message: '未找到面部图层',
        suggestion: '建议添加面部图层'
      });
    }

    const report: QAReport = {
      issues,
      overallScore: Math.max(0, 100 - issues.length * 10),
      passed: input.strictMode ? issues.length === 0 : true
    };

    return {
      report,
      passed: report.passed
    };
  }
}

export default QAStep;
