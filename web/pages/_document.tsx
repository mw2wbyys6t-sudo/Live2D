import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="zh-CN">
      <Head>
        <meta charSet="utf-8" />
        <meta name="description" content="Live2D PSD 质量检测工具 - 在线分析 PSD 文件结构，检测 Live2D 建模风险" />
        <meta name="keywords" content="Live2D, PSD, QA, 质量检测, 模型检测, VTuber" />
        <meta name="author" content="Live2D PSD QA" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
        <meta name="theme-color" content="#0f0f13" />
        <meta name="color-scheme" content="dark" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <link rel="icon" href="/Live2D/favicon.ico" />
        <link rel="apple-touch-icon" href="/Live2D/apple-touch-icon.png" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
