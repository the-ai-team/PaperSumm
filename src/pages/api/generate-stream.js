import { NextApiResponse } from 'next';
import { express } from 'next';
import EventSource from 'eventsource';

export default async function handler(req, res) {
  const endpoint = process.env.SERVER_ENDPOINT;

  // TODO: get url and keyword from query params
  const url = 'https://arxiv.org/abs/1512.03385';
  const keyword = 'Experiment and results';

  res.writeHead(200, {
    Connection: 'keep-alive',
    'Cache-Control': 'no-cache',
    'Content-Type': 'text/event-stream',
  });

  const eventSource = new EventSource(
    `${endpoint}/generate?url=${encodeURIComponent(
      url
    )}&keyword=${encodeURIComponent(keyword)}`
  );

  eventSource.onmessage = (event) => {
    res.json(event.data);
    console.log(JSON.parse(event.data));
  };

  eventSource.onerror = (e) => {
    console.error('Error occurred', e);
    eventSource.close();
    return;
  };
}
