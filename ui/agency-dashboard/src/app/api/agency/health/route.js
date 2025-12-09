import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.AGENCY_BACKEND_URL || 'http://localhost:8000';

export async function GET() {
  try {
    const endpoints = ['/health', '/docs', '/'];
    for (const endpoint of endpoints) {
      try {
        const response = await fetch(`${BACKEND_URL}${endpoint}`, {
          method: 'GET',
          signal: AbortSignal.timeout(2000),
        });
        if (response.ok || response.status === 200 || response.status === 307) {
          return NextResponse.json({ status: 'ok', endpoint });
        }
      } catch {
        continue;
      }
    }
    return NextResponse.json({ status: 'error' }, { status: 503 });
  } catch (error) {
    return NextResponse.json({ status: 'error', message: error.message }, { status: 503 });
  }
}
