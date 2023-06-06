import { NextApiResponse } from 'next';
import { express } from 'next';

export default async function handler(req, res) {
  const endpoint = process.env.SERVER_ENDPOINT;

  const body = {
    url: 'https://arxiv.org/abs/1512.03385',
    keyword: 'Experiment and results',
  };

  const data = await fetch(endpoint + '/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const result = await data.json();

  res.status(200).json({ text: await result });
}
