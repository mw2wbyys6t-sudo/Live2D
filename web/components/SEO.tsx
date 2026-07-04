import Head from 'next/head';

interface SEOProps {
  title?: string;
  description?: string;
  keywords?: string;
}

export default function SEO({
  title = 'Live2D PSD QA - PSD 质量检测工具',
  description = '在线分析 PSD 文件结构，检测 Live2D 建模风险，提供优化建议',
  keywords = 'Live2D, PSD, QA, 质量检测, VTuber, 模型检测',
}: SEOProps) {
  return (
    <Head>
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content="website" />
      <meta name="twitter:card" content="summary" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
    </Head>
  );
}
