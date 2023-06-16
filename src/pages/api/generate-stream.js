import EventSource from 'eventsource';

export default async function handler(req, res) {
  // TODO: get url and keyword from query params
  const url = 'https://arxiv.org/abs/1512.03385';
  const keyword = 'Experiment and results';

  res.writeHead(200, {
    Connection: 'keep-alive',
    'Cache-Control': 'no-cache',
    'Content-Type': 'text/event-stream',
  });
  res.flushHeaders();

  const endpoint = process.env.SERVER_ENDPOINT;
  const address = `${endpoint}/generate?url=${encodeURIComponent(
    url
  )}&keyword=${encodeURIComponent(keyword)}`;
  console.log('address', address);
  const eventSource = new EventSource(address);

  req.on('close', () => {
    console.log('client closed connection');
    eventSource.close();
    return;
  });

  eventSource.addEventListener('content', (event) => {
    console.log('content received');
    res.write(`event: content\ndata: ${JSON.stringify(event.data)}\n\n`);
  });

  eventSource.addEventListener('full-content', (event) => {
    console.log('full-content received');
    res.write(`event: full-content\ndata: ${JSON.stringify(event.data)}\n\n`);
    eventSource.close();
    res.end();
    return;
  });

  eventSource.addEventListener('error', (event) => {
    console.log('error received');
    res.write(`event: error\ndata: ${JSON.stringify(event.data)}\n\n`);
    eventSource.close();
    res.end();
    return;
  });
}
