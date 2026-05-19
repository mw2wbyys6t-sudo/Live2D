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
        id: `qa-${Date.now()}-1`,
        type: 'warning',
        category: 'missing_layer',
        message: '未找到面部图层',
        suggestion: '建议添加面部图层',
        severity: 5
      });
    }

    const report: QAReport = {
      id: `qa-report-${Date.now()}`,
      psdLayerPlanId: input.plan.id,
      issues,
      totalIssues: issues.length,
      criticalCount: issues.filter(i => i.type === 'critical').length,
      warningCount: issues.filter(i => i.type === 'warning').length,
      infoCount: issues.filter(i => i.type === 'info').length,
      score: Math.max(0, 100 - issues.length * 10),
      generatedAt: new Date()
    };

    return {
      report,
      passed: input.strictMode ? issues.length === 0 : issues.filter(i => i.type === 'critical').length === 0
    };
  }
}

export default QAStep;