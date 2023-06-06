import { NextApiResponse } from 'next';
import { express } from 'next';

export default async function handler(req, res) {
  const endpoint = process.env.SERVER_ENDPOINT;

  // TODO: get url and keyword from query params
  const url = 'https://arxiv.org/abs/1512.03385';
  const keyword = 'Experiment and results';

  const eventSource = new EventSource(
    `${endpoint}?url=${encodeURIComponent(url)}&keyword=${encodeURIComponent(
      keyword
    )}`
  );

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Handle the received data
    console.log(data);
  };

  eventSource.onerror = () => {
    // Handle errors
    console.error('Error occurred');
  };

  res.status(200).json({ text: await result });
}
