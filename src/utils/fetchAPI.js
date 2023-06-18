// // should send a post request to the server with the data
// const sampleData = [
//   {
//     Title: 'Introduction of Deep Residual Learning Framework',
//     Content:
//       'The paper introduces a deep residual learning framework to address the degradation problem caused by increasing network depth. The framework involves explicitly letting stacked layers fit a residual mapping, which can be realized by feedforward neural networks with "shortcut connections". The shortcut connections perform identity mapping and add neither extra parameter nor computational complexity.',
//   },
//   {
//     Title: 'Effectiveness of Residual Learning Framework',
//     Content:
//       'The paper provides comprehensive empirical evidence showing the effectiveness of the deep residual learning framework. The authors tested various plain and residual networks and observed consistent phenomena. They describe two models for ImageNet: a plain network inspired by VGG nets and a residual network with shortcut connections. The residual network outperformed the plain network on both training and validation sets. The authors also conducted experiments on CIFAR-10 and CIFAR-100 datasets, showing that the residual networks consistently outperformed the plain networks. The authors suggest that the success of residual networks may be due to their ability to address the degradation problem and make it easier for solvers to find perturbations with reference to an identity mapping.',
//     Diagrams: {
//       Type: 'img',
//       Figure: ['https://ar5iv.labs.arxiv.org/html/1512.03385/assets/x1.png'],
//       Description:
//         'Figure 1: Training error (left) and test error (right) on CIFAR-10 with 20-layer and 56-layer "plain" networks. The deeper network has higher training error, and thus test error. Similar phenomena on ImageNet is presented in Fig.\xa04.',
//     },
//   },
//   {
//     Title: 'Experiments on ImageNet and CIFAR-10 datasets',
//     Content:
//       'The paper presents successful experiments on ImageNet and CIFAR-10 datasets, with the 152-layer residual net being the deepest network ever presented on ImageNet. The ensemble of residual nets achieves 3.57% error on the ImageNet test set and wins the 1st place in the ILSVRC 2015 classification competition, as well as other recognition tasks. The implementation for ImageNet follows the practice in previous works. The image is resized with its shorter side randomly sampled in 256-480 for scale augmentation. A 224x224 crop is randomly sampled from an image or its horizontal flip, with the per-pixel mean subtracted. Batch normalization (BN) is used right after each convolution and before activation.',
//     Diagrams: {
//       Type: 'img',
//       Figure: [
//         'https://ar5iv.labs.arxiv.org/html/1512.03385/assets/x1.png',
//         'https://ar5iv.labs.arxiv.org/html/1512.03385/assets/x1.png',
//       ],
//       Description:
//         'Figure 1: Training error (left) and test error (right) on CIFAR-10 with 20-layer and 56-layer "plain" networks. The deeper network has higher training error, and thus test error. Similar phenomena on ImageNet is presented in Fig.\xa04.',
//     },
//   },
//   {
//     Title: 'Deep Residual Networks Architecture',
//     Content:
//       'Plain and residual networks are evaluated, with the latter showing better performance on deeper networks. Identity shortcuts are found to be important for not increasing the complexity of the bottleneck architectures. Deeper bottleneck architectures are constructed, resulting in 50-layer, 101-layer, and 152-layer ResNets. The 152-layer ResNet achieves a single-model top-5 validation error of 4.49%, outperforming all previous ensemble results. The focus is on the behaviors of extremely deep networks, but not on pushing the state-of-the-art results. The network architecture consists of a stack of 6n layers with 3x3 convolutions on feature maps of sizes 32, 16, and 8, with 2n layers for each feature map size. The numbers of filters are 16, 32, and 64 respectively. The network ends with global average pooling, a 10-way fully-connected layer, and softmax. There are a total of 6n+2 stacked weighted layers. Identity shortcuts are used in all cases. The network is trained with a mini-batch size of 128 on two GPUs, with a weight decay of 0.0001 and momentum of 0.9, and no dropout. The learning rate starts at 0.1, is divided by 10 at 32k and 48k iterations, and training is terminated at 64k iterations. The network is trained with simple data augmentation, such as padding and cropping.',
//   },
//   {
//     Title: ' Experiments on Object Detection ',
//     Content:
//       'ResNet-101 improves the mAP by >>>3% over VGG-16 on the PASCAL VOC dataset. ResNet-based detection models win 1st place in several tracks in ILSVRC & COCO 2015 competitions. The COCO models are trained with an 8-GPU implementation, with a mini-batch size of 8 images for the RPN step and 16 images for the Fast R-CNN step. The RPN and Fast R-CNN steps are trained for 240k iterations with a learning rate of 0.001 and then for 80k iterations with 0.0001. ResNet-101 shows a 6% increase in mAP@[.5, .95] over VGG-16, which is a 28% relative improvement, solely contributed by the features learned by the better network. Box refinement, global context, and multi-scale testing are used to improve the mAP. Using the 80k+40k trainval set for training and the 20k test-dev set for evaluation, the single-model result achieves an mAP@.5 of 55.7% and an mAP@[.5, .95] of 34.9%. An ensemble of 3 networks achieves an mAP of 59.0% and 37.4% on the test-dev set, winning the 1st place in the detection task in COCO 2015. The same model is fine-tuned on the PASCAL VOC sets, achieving 85.6% mAP on PASCAL VOC 2007 and 83.8% on PASCAL VOC 2012. For the ImageNet Detection task, the same object detection algorithm as for MS COCO is used, achieving 58.8% mAP for the single model and 62.1% mAP for the ensemble of 3 models on the DET test set, winning the 1st place in ILSVRC 2015. For the ImageNet Localization task, the RPN method using ResNet-101 significantly reduces the center-crop error to 13.3%, and with dense and multi-scale testing, the error is reduced to 11.7%. Using ResNet-101 for predicting classes, the top-5 localization error is 14.4%.',
//   },
// ];

// const fetchData = async () => {
//   try {
//     const response = await fetch('/api/generate'); // Replace with the actual URL of your edge function
//     if (response.ok) {
//       const data = await response.json();
//       console.log(data.message);
//     } else {
//       console.error('Error:', response.status);
//     }
//   } catch (error) {
//     console.error('Error:', error);
//   }
// };
//
// fetchData();
//

// export const fetchAPI = async ({ url, keyword }) => {
//   // FOR TESTING PURPOSES
//   // const response = new Promise((resolve, reject) => {
//   //   setTimeout(() => {
//   //     resolve(sampleData);
//   //   }, 6000);
//   // });
//   try {
//     const endpoint = `/api/generate`;
//     const data = {
//       url,
//       keyword: keyword[0],
//     };
//     console.log(JSON.stringify(data));
//     const response = await fetch(endpoint, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "Access-Control-Allow-Origin": "*",
//       },
//       body: JSON.stringify(data),
//     });
//     console.log(response.json());
//     return await response.json();
//   } catch (e) {
//     console.error(e);
//   }
// };
function validateSampleData(data) {
  if (!data) {
    // "Data is undefined."
    console.warn('Data is undefined.');
    return [false];
  }

  if (!Array.isArray(data)) {
    // "Data is not an array."
    console.warn('Data is not an array.');
    return [false];
  }

  for (const item of data) {
    if (item.Error) {
      console.warn(item.Error);
      return [false, item.Error];
    }

    if (!item.Title || typeof item.Title !== 'string') {
      // "Invalid or missing 'Title' field."
      console.warn("Invalid or missing 'Title' field.");
      return [false];
    }

    if (!item.Content || typeof item.Content !== 'string') {
      // "Invalid or missing 'Content' field."
      console.warn("Invalid or missing 'Content' field.");
      return [false];
    }

    if (item.Diagrams) {
      if (typeof item.Diagrams !== 'object') {
        // "Invalid 'Diagrams' field."
        console.warn("Invalid 'Diagrams' field.");
        return [false];
      }

      if (!item.Diagrams.Type || typeof item.Diagrams.Type !== 'string') {
        // "Invalid or missing 'Diagrams.Type' field."
        console.warn("Invalid or missing 'Diagrams.Type' field.");
        return [false];
      }

      if (!item.Diagrams.Figure || !Array.isArray(item.Diagrams.Figure)) {
        // "Invalid or missing 'Diagrams.Figure' field."
        console.warn("Invalid or missing 'Diagrams.Figure' field.");
        return [false];
      }

      if (
        !item.Diagrams.Description ||
        typeof item.Diagrams.Description !== 'string'
      ) {
        // return "Invalid or missing 'Diagrams.Description' field."
        console.warn("Invalid or missing 'Diagrams.Description' field.");
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

export const fetchAPI = async ({ updateSummary, setError }) => {
  const endpoint = 'http://localhost:3000/api/generate-stream';
  eventSource = new EventSource(endpoint);

  const summary = [];
  let currentIndex = -1;

  console.time('fetchAPI');
  try {
    eventSource.addEventListener('content', (event) => {
      const content = JSON.parse(event.data);

      if (!Array.isArray(content)) {
        console.error('Invalid content received, not an array');
        // TODO: throw errors
        return;
      }

      for (const item of content) {
        if (!item.content_type) {
          console.error('Invalid content received, content_type is missing');
          return;
        }

        const contentType = item.content_type;

        if (contentType !== ContentType[0] && contentType !== ContentType[1]) {
          console.error('Invalid content received, content_type is invalid');
          return;
        }

        // only if it's not a delimiter
        let contentIndex;
        const contentText = item.text;

        // Validate content index
        try {
          contentIndex = parseInt(item.index);
          console.log('contentIndex', contentIndex);
        } catch (e) {
          console.error(
            'Invalid content received, content_index is not a number'
          );
          return;
        }

        if (contentIndex < 0) {
          console.error('Invalid content received, content_index is negative');
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
          console.log('title', contentText);

          contentText.split('').forEach(async (letter) => {
            summary[contentIndex].title += letter;
            // await sleep(10000);
            updateSummary({ valid: true, value: summary });
          });
        }
        if (contentType === 'paragraph') {
          console.log('paragraph', contentText);

          contentText.split('').forEach(async (letter) => {
            summary[contentIndex].content += letter;
            // console.log(letter);
            // await sleep(10000);
            updateSummary({ valid: true, value: summary });
          });
        }

        console.log('content collected');
      }
    });

    eventSource.addEventListener('full-content', (event) => {
      console.log('full-content received');
      eventSource.close();
    });

    eventSource.addEventListener('error', (event) => {
      console.log(event.data);
      if (event.data) {
        try {
          setError(JSON.parse(event.data));
        } catch (error) {}
      }
      eventSource.close();
    });

    console.timeEnd('fetchAPI');
  } catch (e) {
    console.error(e);
    setError('Client error.');
    console.timeEnd('fetchAPI');
  }
};

const handleData = (data) => {
  console.log(data);

  if (data.type === 'content') {
    console.log(data.content);
  }
};
