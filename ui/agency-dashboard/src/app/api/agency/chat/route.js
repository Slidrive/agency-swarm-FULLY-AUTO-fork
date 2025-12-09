import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.AGENCY_BACKEND_URL || 'http://localhost:8000';

export async function POST(request) {
  try {
    const body = await request.json();

    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(process.env.AGENCY_CLIENT_API_KEY && {
          'X-API-Key': process.env.AGENCY_CLIENT_API_KEY,
        }),
      },
      body: JSON.stringify({
        message: body.message,
        thread_id: body.thread_id || null,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json({ error: `Backend error: ${response.status}`, details: errorText }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to connect to backend', message: error.message }, { status: 503 });
  }
}
