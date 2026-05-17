import type { AppProps } from 'next/app';
import { useEffect } from 'react';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/Live2D/sw.js').catch(() => {
        // 静默处理 Service Worker 注册失败
      });
    }
  }, []);

  return <Component {...pageProps} />;
}
