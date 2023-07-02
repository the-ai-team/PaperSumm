import EventSource from 'eventsource';

export default async function handler(req, res) {
  const { url, keyword } = req.query;
  console.log('query', req.query);

  // const url = 'https://arxiv.org/abs/1512.03385';
  // const keyword = 'Experiment and results';
  res.writeHead(200, {
    Connection: 'keep-alive',
    'Cache-Control': 'no-cache',
    'Content-Type': 'text/event-stream',
  });

  const endpoint = process.env.SERVER_ENDPOINT;
  const address = `${endpoint}/generate?url=${encodeURIComponent(
    url
  )}&keyword=${encodeURIComponent(keyword)}`;
  const eventSource = new EventSource(address);

  eventSource.addEventListener('content', (event) => {
    console.log('content received');
    res.write(`event: content\ndata: ${event.data}\nretry: 1000\n\n`);
  });

  eventSource.addEventListener('full-content', (event) => {
    console.log('full-content received');
    res.write(`event: full-content\ndata: ${event.data}\nretry: 1000\n\n`);
    eventSource.close();
    res.end();
    return;
  });

  eventSource.addEventListener('error', (event) => {
    res.write(`event: error\ndata: ${event.data}\nretry: 1000\n\n`);
    eventSource.close();
    res.end();
    return;
  });
}
