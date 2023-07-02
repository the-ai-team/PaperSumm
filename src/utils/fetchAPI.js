function validateSampleData(data) {
  if (!data) {
    // "Data is undefined."
    // console.warn('Data is undefined.');
    return [false];
  }

  if (!Array.isArray(data)) {
    // "Data is not an array."
    // console.warn('Data is not an array.');
    return [false];
  }

  for (const item of data) {
    if (item.Error) {
      // console.warn(item.Error);
      return [false, item.Error];
    }

    if (!item.Title || typeof item.Title !== 'string') {
      // "Invalid or missing 'Title' field."
      // console.warn("Invalid or missing 'Title' field.");
      return [false];
    }

    if (!item.Content || typeof item.Content !== 'string') {
      // "Invalid or missing 'Content' field."
      // console.warn("Invalid or missing 'Content' field.");
      return [false];
    }

    if (item.Diagrams) {
      if (typeof item.Diagrams !== 'object') {
        // "Invalid 'Diagrams' field."
        // console.warn("Invalid 'Diagrams' field.");
        return [false];
      }

      if (!item.Diagrams.Type || typeof item.Diagrams.Type !== 'string') {
        // "Invalid or missing 'Diagrams.Type' field."
        // console.warn("Invalid or missing 'Diagrams.Type' field.");
        return [false];
      }

      if (!item.Diagrams.Figure || !Array.isArray(item.Diagrams.Figure)) {
        // "Invalid or missing 'Diagrams.Figure' field."
        // console.warn("Invalid or missing 'Diagrams.Figure' field.");
        return [false];
      }

      if (
        !item.Diagrams.Description ||
        typeof item.Diagrams.Description !== 'string'
      ) {
        // return "Invalid or missing 'Diagrams.Description' field."
        // console.warn("Invalid or missing 'Diagrams.Description' field.");
        return [false];
      }
    }
  }
  return [true];
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const ContentType = {
  0: 'title',
  1: 'paragraph',
  2: 'delimiter',
};

export let eventSource = null;

export const fetchAPI = async ({ url, keyword, updateSummary, setError }) => {
  const endpoint = '/api/generate-stream';
  const address = `${endpoint}?url=${encodeURIComponent(
    url
  )}&keyword=${encodeURIComponent(keyword)}`;

  eventSource = new EventSource(address);

  const summary = [];
  let currentIndex = -1;

  // console.time('fetchAPI');
  try {
    eventSource.addEventListener('content', (event) => {
      const content = JSON.parse(event.data);

      if (!Array.isArray(content)) {
        // console.error('Invalid content received, not an array');
        return;
      }

      for (const item of content) {
        if (!item.content_type) {
          // console.error('Invalid content received, content_type is missing');
          return;
        }

        const contentType = item.content_type;

        if (contentType !== ContentType[0] && contentType !== ContentType[1]) {
          // console.error('Invalid content received, content_type is invalid');
          return;
        }

        // only if it's not a delimiter
        let contentIndex;
        const contentText = item.text;

        // Validate content index
        try {
          contentIndex = parseInt(item.index);
          // console.log('contentIndex', contentIndex);
        } catch (e) {
          // console.error(
          //   'Invalid content received, content_index is not a number'
          // );
          return;
        }

        if (contentIndex < 0) {
          // console.error('Invalid content received, content_index is negative');
          return;
        }

        if (contentIndex > currentIndex) {
          while (contentIndex > currentIndex) {
            summary.push({ title: '', content: '' });
            currentIndex++;
          }
        }
        // ==== //

        // Add content to summary
        if (contentType === 'title') {
          // console.log('title', contentText);

          contentText.split('').forEach(async (letter) => {
            summary[contentIndex].title += letter;
            // await sleep(10000);
            updateSummary({ valid: true, value: summary });
          });
        }
        if (contentType === 'paragraph') {
          // console.log('paragraph', contentText);

          contentText.split('').forEach(async (letter) => {
            summary[contentIndex].content += letter;
            // console.log(letter);
            // await sleep(10000);
            updateSummary({ valid: true, value: summary });
          });
        }

        // console.log('content collected');
      }
    });

    eventSource.addEventListener('full-content', (event) => {
      eventSource.close();

      const content = JSON.parse(event.data);
      // console.log('full-content', content);

      if (!Array.isArray(content)) {
        return;
      }

      content.forEach((item, index) => {
        if (item?.diagrams) {
          const diagrams = item.diagrams;

          updateSummary({
            valid: true,
            value: summary.map((item, i) => {
              if (i === index) {
                return {
                  ...item,
                  diagrams,
                };
              }
              return item;
            }),
          });
        }
      });
    });

    eventSource.addEventListener('error', (event) => {
      // console.log(event.data);
      if (event.data) {
        try {
          setError(JSON.parse(event.data));
        } catch (error) {
          setError('Something went wrong.');
        }
      }
      eventSource.close();
    });

    // console.timeEnd('fetchAPI');
  } catch (e) {
    // console.error(e);
    setError('Client error.');
    // console.timeEnd('fetchAPI');
  }
};
