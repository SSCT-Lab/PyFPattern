@evaluator(EvaluatorAttribute.FOR_CLASSIFICATION)
@wrap_name_default()
def chunk_evaluator(input, label, chunk_scheme, num_chunk_types, name=None, excluded_chunk_types=None):
    '\n    Chunk evaluator is used to evaluate segment labelling accuracy for a\n    sequence. It calculates precision, recall and F1 scores for the chunk detection.\n\n    To use chunk evaluator, several concepts need to be clarified firstly.\n\n    * **Chunk type** is the type of the whole chunk and a chunk consists of one or several words.  (For example in NER, ORG for organization name, PER for person name etc.)\n\n    * **Tag type** indicates the position of a word in a chunk. (B for begin, I for inside, E for end, S for single)\n    We can name a label by combining tag type and chunk type. (ie. B-ORG for begining of an organization name)\n\n    The construction of label dictionary should obey the following rules:\n\n    - Use one of the listed labelling schemes. These schemes differ in ways indicating chunk boundry.\n\n    .. code-block:: text\n\n        Scheme    Description                                                                                  \n        plain    Use the same label for the whole chunk.\n        IOB      Two labels for chunk type X, B-X for chunk begining and I-X for chunk inside. \n        IOE      Two labels for chunk type X, E-X for chunk ending and I-X for chunk inside.\n        IOBES    Four labels for chunk type X, B-X for chunk begining, I-X for chunk inside, E-X for chunk end and S-X for single word chunk. \n   \n    To make it clear, let\'s illustrate by an NER example.\n    Assuming that there are three named entity types including ORG, PER and LOC which are called \'chunk type\' here,\n    if \'IOB\' scheme were used, the label set will be extended to a set including B-ORG, I-ORG, B-PER, I-PER, B-LOC, I-LOC and O,\n    in which B-ORG for begining of ORG and I-ORG for inside of ORG.\n    Prefixes which are called \'tag type\' here are added to chunk types and there are two tag types including B and I.\n    Of course, the training data should be labeled accordingly.\n\n    - Mapping is done correctly by the listed equations and assigning protocol.\n\n    The following table are equations to extract tag type and chunk type from a label.\n\n    .. code-block:: text\n\n        tagType = label % numTagType\n        chunkType = label / numTagType\n        otherChunkType = numChunkTypes\n    \n    The following table shows the mapping rule between tagType and tag type in each scheme.\n\n    .. code-block:: text\n\n        Scheme Begin Inside End   Single\n        plain  0     -      -     -\n        IOB    0     1      -     -\n        IOE    -     0      1     -\n        IOBES  0     1      2     3\n\n    Continue the NER example, and the label dict should look like this to satify above equations:\n\n    .. code-block:: text\n\n        B-ORG  0\n        I-ORG  1\n        B-PER  2\n        I-PER  3\n        B-LOC  4\n        I-LOC  5\n        O      6\n\n    In this example, chunkType has three values: 0 for ORG, 1 for PER, 2 for LOC, because the scheme is\n    "IOB" so tagType has two values: 0 for B and 1 for I. \n    Here we will use I-LOC to explain the above mapping rules in detail.\n    For I-LOC, the label id is 5, so we can get tagType=1 and chunkType=2, which means I-LOC is a part of NER chunk LOC\n    and the tag is I.\n\n    The simple usage is:\n\n    .. code-block:: python\n\n       eval = chunk_evaluator(input, label, chunk_scheme, num_chunk_types)\n\n    \n    :param input: The input layers.\n    :type input: LayerOutput\n    :param label: An input layer containing the ground truth label.\n    :type label: LayerOutput\n    :param chunk_scheme: The labelling schemes support 4 types. It is one of\n                         "IOB", "IOE", "IOBES", "plain". It is required.\n    :type chunk_scheme: basestring\n    :param num_chunk_types: number of chunk types other than "other"\n    :param name: The Evaluator name, it is optional.\n    :type name: basename|None\n    :param excluded_chunk_types: chunks of these types are not considered\n    :type excluded_chunk_types: list of integer|None\n    '
    evaluator_base(name=name, type='chunk', input=input, label=label, chunk_scheme=chunk_scheme, num_chunk_types=num_chunk_types, excluded_chunk_types=excluded_chunk_types)