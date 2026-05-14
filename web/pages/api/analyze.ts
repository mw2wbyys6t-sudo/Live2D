import type { NextApiRequest, NextApiResponse } from 'next';
import { parsePSD } from '../../lib/psd-parser';
import { analyzePSD, QAResult } from '../../lib/qa-engine';

export const config = {
  api: {
    bodyParser: false,
    maxBodySize: 52428800,
  },
};

interface AnalyzeResponse {
  success: boolean;
  data?: QAResult;
  fileInfo?: {
    name: string;
    size: number;
    width: number;
    height: number;
  };
  error?: string;
}

function parseMultipartBody(buffer: Buffer, boundary: string) {
  const fields: Record<string, string> = {};
  const files: Record<string, { name: string; data: Buffer; type: string }> = {};
  const parts = buffer.toString('binary').split(`--${boundary}`);

  for (const part of parts) {
    if (part.includes('Content-Disposition')) {
      const headerEnd = part.indexOf('\r\n\r\n');
      if (headerEnd === -1) continue;

      const headers = part.substring(0, headerEnd);
      const body = part.substring(headerEnd + 4);

      const nameMatch = headers.match(/name="([^"]+)"/);
      if (!nameMatch) continue;

      const fieldName = nameMatch[1];

      if (headers.includes('filename=')) {
        const filenameMatch = headers.match(/filename="([^"]+)"/);
        const typeMatch = headers.match(/Content-Type:\s*(\S+)/);
        const filename = filenameMatch ? filenameMatch[1] : 'unknown';

        const rawData = Buffer.from(body, 'binary');
        const cleanData = rawData.slice(0, rawData.length - 2);

        files[fieldName] = {
          name: filename,
          data: cleanData,
          type: typeMatch ? typeMatch[1] : 'application/octet-stream',
        };
      } else {
        const value = body.replace(/\r\n$/, '');
        fields[fieldName] = value;
      }
    }
  }

  return { fields, files };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<AnalyzeResponse>
) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    res.status(405).json({ success: false, error: `Method ${req.method} not allowed` });
    return;
  }

  try {
    const contentType = req.headers['content-type'] || '';
    if (!contentType.includes('multipart/form-data')) {
      res.status(400).json({ success: false, error: 'Content-Type must be multipart/form-data' });
      return;
    }

    const boundaryMatch = contentType.match(/boundary=(.+)/);
    if (!boundaryMatch) {
      res.status(400).json({ success: false, error: 'No boundary found in Content-Type' });
      return;
    }

    const chunks: Buffer[] = [];
    for await (const chunk of req) {
      chunks.push(chunk);
    }
    const buffer = Buffer.concat(chunks);

    const parsed = parseMultipartBody(buffer, boundaryMatch[1]);
    const psdFile = parsed.files['psd'];

    if (!psdFile) {
      res.status(400).json({ success: false, error: 'No PSD file uploaded' });
      return;
    }

    if (!psdFile.name.toLowerCase().endsWith('.psd')) {
      res.status(400).json({ success: false, error: 'File must be a .psd file' });
      return;
    }

    if (psdFile.data.length < 26) {
      res.status(400).json({ success: false, error: 'Invalid PSD file: too small' });
      return;
    }

    const psdInfo = parsePSD(psdFile.data);

    if (!psdInfo.valid) {
      res.status(400).json({
        success: false,
        error: psdInfo.error || 'Failed to parse PSD file',
      });
      return;
    }

    const qaResult = analyzePSD(psdInfo);

    res.status(200).json({
      success: true,
      data: qaResult,
      fileInfo: {
        name: psdFile.name,
        size: psdFile.data.length,
        width: psdInfo.width,
        height: psdInfo.height,
      },
    });
  } catch (error: any) {
    console.error('PSD analysis error:', error);
    res.status(500).json({
      success: false,
      error: `Analysis failed: ${error.message}`,
    });
  }
}