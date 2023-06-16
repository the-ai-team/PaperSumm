import asyncio
import copy
import json
from random import sample
from core.embeddings import openai
import concurrent.futures
import time

from openai.embeddings_utils import distances_from_embeddings

info = """
1. The paper introduces a deep residual learning framework to address the degradation pr
oblem caused by increasing network depth in deep convolutional neural networks.

2. The framework reformulates layers as learning residual functions with reference to th
e layer inputs, instead of learning unreferenced functions.

3. The authors provide comprehensive empirical evidence showing that these residual 
networks are easier to optimize and can gain accuracy from considerably increased depth.

4. On the ImageNet dataset, the authors evaluate residual nets with a depth of up to 
152 layers, which is 8 times deeper than VGG nets but still has lower complexity.

5. An ensemble of these residual nets achieves 3.57% error on the ImageNet test set, 
winning the 1st place on the ILSVRC 2015 classification task.

6. The authors also present analysis on CIFAR-10 with 100 and 1000 layers, showing 
similar phenomena and suggesting that the optimization difficulties and the effects of 
their method are not just specific to a particular dataset.

7. The extremely deep representations also have excellent generalization performance on 
other recognition tasks, leading to the authors winning the 1st places on ImageNet detection, ImageNet localization, COCO detection, and COCO segmentation in ILSVRC & COCO 2015 competitions.

8. The residual learning principle is shown to be generic and applicable in other vision and non-vision problems.
- The authors conducted experiments to compare plain and residual networks.
- They observed consistent phenomena across various models.
- The plain network had fewer filters and lower complexity than VGG nets.
- The residual network was created by inserting shortcut connections.
- Identity shortcuts were used when input and output dimensions were the same.
- When dimensions increased, two options were considered: identity mapping with zero padding or projection shortcut using 1x1 convolutions.
- The authors found that the learned residual functions generally had small responses, suggesting that identity mappings provided reasonable preconditioning.
- The implementation for ImageNet follows the practice in previous studies.
- The image is resized with its shorter side randomly sampled in 256-480 for scale augmentation.
- A 224x224 crop is randomly sampled from an image or its horizontal flip, with the per-pixel mean subtracted.
- Batch normalization (BN) is used right after each convolution and before activation.
- Plain networks are evaluated first, with 18-layer and 34-layer architectures. The 34-layer plain net has higher validation error than the shallower 18-layer plain net, and the deeper plain nets may have exponentially low convergence rates.
- Residual networks are evaluated next, with 18-layer and 34-layer architectures. The 34-layer ResNet is better than the 18-layer ResNet, and the degradation problem is well addressed in this setting.
- Identity shortcuts are particularly important for not increasing the complexity of the bottleneck architectures that are introduced next.
- Deeper bottleneck architectures are introduced with 50-layer, 101-layer, and 152-layer ResNets, using more 3-layer blocks.
- The 152-layer ResNet has a single-model top-5 validation error of 4.49%, outperforming all previous ensemble results.
- Experiments on the CIFAR-10 dataset focus on the behaviors of extremely deep networks, using simple architectures.
- The authors used a stack of 6n layers with 3x3 convolutions on feature maps of sizes 32, 16, and 8, with 2n layers for each feature map size. The numbers of filters were 16, 32, and 64, respectively.
- The subsampling was performed by convolutions with a stride of 2.
- The network ended with global average pooling, a 10-way fully-connected layer, and softmax.
- There were a total of 6n+2 stacked weighted layers.
- The authors used identity shortcuts in all cases (option A), so the residual models had the same depth, width, and number of parameters as the plain counterparts.
- The models were trained with a weight decay of 0.0001 and momentum of 0.9, and no dropout.
- The authors used a mini-batch size of 128 on two GPUs.
- The learning rate started at 0.1, was divided by 10 at 32k and 48k iterations, and training was terminated at 64k iterations.
- The models were trained with simple data augmentation, including padding and random cropping.
- The authors compared networks with n=3,5,7,9, leading to 20, 32, 44, and 56-layer networks.
- The deep plain nets suffered from increased depth and exhibited higher training error when going deeper.
- The ResNets managed to overcome the optimization difficulty and demonstrated accuracy gains when the depth increased.
- The authors explored n=18, which led to a 110-layer ResNet that converged well.
- The authors explored an aggressively deep model of over 1000 layers and set n=200, which led to a 1202-layer network that achieved training error <<<0.1%.
- The authors won first places in several tracks in ILSVRC & COCO 2015 competitions using deep residual nets.
- The authors used ResNet-101 for object detection on PASCAL VOC and COCO datasets and achieved significant improvements in mAP.
- COCO models are trained with an 8-GPU implementation, with a mini-batch size of 8 images for RPN step and 16 images for Fast R-CNN step.
- The RPN step and Fast R-CNN step are both trained for 240k iterations with a learning rate of 0.001 and then for 80k iterations with 0.0001.
- ResNet-101 has a 6% increase of mAP@[.5, .95] over VGG-16, which is a 28% relative improvement, solely contributed by the features learned by the better network.
- Box refinement improves mAP by about 2 points, global context improves mAP@.5 by about 1 point, and multi-scale testing improves the mAP by over 2 points.
- Using the 80k+40k trainval set for training and the 20k test-dev set for evaluation, the results are an mAP@.5 of 55.7% and an mAP@[.5, .95] of 34.9%.
- An ensemble of 3 networks achieves an mAP of 59.0% and 37.4% on the test-dev set, winning the 1st place in the detection task in COCO 2015.
- Fine-tuning the model on PASCAL VOC sets with the improvements of box refinement, context, and multi-scale testing achieves 85.6% mAP on PASCAL VOC 2007 and 83.8% on PASCAL VOC 2012.
- In ImageNet Detection task, the single model with ResNet-101 has 58.8% mAP and the ensemble of 3 models has 62.1% mAP on the DET test set, winning the 1st place in ILSVRC 2015.
- In ImageNet Localization task, the RPN method using ResNet-101 reduces the center-crop error to 13.3%, and with dense and multi-scale testing, the error is 11.7% using ground truth classes.
"""  # noqa: E501

sample_context = [
    {"type": "content", "content": []},
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "Introduction", "index": 0},
        ],
    },
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "and", "index": 0},
        ],
    },
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "Framework", "index": 0},
        ],
    },
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "section-del"},
        ],
    },
    {
        "type": "content",
        "content": [{"content_type": "paragraph", "text": "The", "index": 0}],
    },
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "paper", "index": 0},
        ],
    },
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "introduces", "index": 0},
        ],
    },
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "a", "index": 0},
        ],
    },
    {
        "type": "content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "deep", "index": 0},
        ],
    },
    {
        "type": "full-content",
        "content": [
            {"content_type": "paragraph", "text": " ", "index": 0},
            {"content_type": "paragraph", "text": "deep", "index": 0},
        ],
    },
]


# def get_related_info(keyword, context):
#     """
#     Extract related information from the context
#     """
#     response = openai.ChatCompletion.create(  # Create a completions using the keyword and context
#         messages=[{
#             "role": "user",
#             "content": f"""
#                     Extract information most related to {keyword} of the following context which was taken from a research paper\n
#                     context : {context}\n
#                     points :
#                     """
#         }],
#         temperature=0.5,
#         max_tokens=1024,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#         model="gpt-3.5-turbo",
#     )
#     return response["choices"][0]["message"]["content"].strip()


def generate_content_with_stream(
    context, keyword, model="gpt-3.5-turbo", stop_sequence=None
):
    print("Generating content")

    """
    Generate content based on the generated points of the paper
    """
    responses = openai.ChatCompletion.create(  # Create a completions using the keyword and context
        # TODO: remove text limit
        messages=[
            {
                "role": "user",
                "content": f"""
                Organize the following points related to {keyword} of a research by dividing into suitable subtopics. 
                Generate a summarized paragraph for each subtopic (max 10 words).\n\n use this format,\n ## generated subtopic ##\n 
                <Summarized paragraph under the subtopic>\n\n points: {context} 
                organized document:
                 """,
            }
        ],
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop_sequence,
        model=model,
        stream=True,
    )

    for response in responses:
        data = response["choices"][0]["delta"]
        if "content" in data:
            content = data["content"]
            yield content


# content_dicts = []
# content_dict_temp = {}
# content_type = {
#     0: "title",
#     1: "paragraph"
# }
# content_type_selected = 1
# content_temp = ""
# titles_count = 0
# paragraphs_count = 0


class ContentMetadata:
    def __init__(self):
        self.content_dicts = []
        self.content_dict_temp = {}
        self.content_type = {0: "title", 1: "paragraph"}
        self.content_type_selected = 1
        self.content_temp = ""
        self.titles_count = 0
        self.paragraphs_count = 0


def generate_content_dict_stream(content, content_metadata):
    """
    Create a dictionary of generated content by sections

    Chunk format -
    {
        content_type: 'title' OR 'para',
        text: ''
        index: {number}
    }

    Paragaph delimiter (between sections) format -
    {
        content_type: 'delimeter'
    }
    """
    content = content.replace("\n", "")

    output = []

    for string_chunk in content.split(" "):
        if string_chunk == "##":
            # Add block of temporary stored content to the dictionary
            if content_metadata.content_temp != "":
                content_metadata.content_dict_temp[
                    content_metadata.content_type[
                        content_metadata.content_type_selected
                    ]
                ] = content_metadata.content_temp
                if content_metadata.content_type_selected == 1:
                    content_metadata.content_dicts.append(
                        copy.deepcopy(content_metadata.content_dict_temp)
                    )

                    output_data = {
                        "content_type": "delimeter",
                    }
                    output.append(output_data)

            # Reset temporary content
            content_metadata.content_temp = ""

            # Toggle content type
            content_metadata.content_type_selected = (
                1 if content_metadata.content_type_selected == 0 else 0
            )

            print("toggle content type")

            # Increment counters
            if content_metadata.content_type_selected == 0:
                content_metadata.titles_count += 1
            else:
                content_metadata.paragraphs_count += 1

            continue
        else:
            # output content
            if string_chunk == "":
                content_metadata.content_temp += " "

                output_data = {
                    "content_type": content_metadata.content_type[
                        content_metadata.content_type_selected
                    ],
                    "text": " ",
                    "index": content_metadata.titles_count
                    if content_metadata.content_type_selected == 0
                    else content_metadata.paragraphs_count,
                }
                output.append(output_data)

            else:
                content_metadata.content_temp += string_chunk

                output_data = {
                    "content_type": content_metadata.content_type[
                        content_metadata.content_type_selected
                    ],
                    "text": string_chunk,
                    "index": content_metadata.titles_count
                    if content_metadata.content_type_selected == 0
                    else content_metadata.paragraphs_count,
                }
                output.append(output_data)

    return output, content_metadata


def match_diagrams(diagrams_df, generated_content_dict, threshold=0.15):
    """
    match diagrams for each generated section
    """
    for section in generated_content_dict:
        content_embeddings = openai.Embedding.create(
            input=section["paragraph"], engine="text-embedding-ada-002"
        )["data"][0][
            "embedding"
        ]  # Get Embeddings
        diagrams_df["Distances"] = distances_from_embeddings(
            content_embeddings,
            diagrams_df["Embeddings"].values,
            distance_metric="cosine",
        )  # Get the distances from the embeddings

        diagrams_df = diagrams_df.sort_values(
            "Distances", ascending=True
        )  # sort ascending as distances

        if diagrams_df["Distances"][0] < threshold:
            section["diagrams"] = {
                "type": diagrams_df["Type"][0],
                "figure": diagrams_df["Figure"][0],
                "description": diagrams_df["Text"][0],
            }
            # diagrams_df = diagrams_df.drop(index = 0)

    return generated_content_dict


def Generate(content_df, diagrams_df, keyword):
    """
    Main function for generating
    """
    # information = [None] * len(content_df)  # Initialize the list with None values
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = {}
    #     for i, row in content_df.iterrows():
    #         context = row["Text"]
    #         keyword = keyword
    #         futures[executor.submit(get_related_info, context, keyword)] = i  # Use a dictionary to associate each future with an index
    #     for future in concurrent.futures.as_completed(futures):
    #         i = futures[future]  # Get the index associated with the completed future
    #         information[i] = future.result()  # Add the result to the appropriate index in the list
    #
    # related_information = ("\n").join(information)
    # print(related_information)

    # generated_content = generate_content(related_information,keyword)
    generated_content = generate_content_with_stream(info, keyword)
    # print(generated_content)

    # set metadata
    content_metadata = {}
    content_metadata["content_dicts"] = []
    content_metadata["content_dict_temp"] = {}
    content_metadata["content_type_selected"] = 1
    content_metadata["content_temp"] = ""
    content_metadata["titles_count"] = 0
    content_metadata["paragraphs_count"] = 0

    for generated_content_chunk in generated_content:
        content_metadata = ContentMetadata()

        (
            generated_content_output,
            updated_metadata,
        ) = generate_content_dict_stream(generated_content_chunk, content_metadata)
        output = {"type": "content", "content": generated_content_output}
        yield output

    # full_output = {
    #     "type": "full-content",
    #     "content": match_diagrams(
    #         diagrams_df, updated_metadata.content_dicts
    #     ),  # match diagrams
    # }
    # yield full_output

    # for content in sample_context:
    #     yield content
