class PromptTemplates:
    # Stage 0 prompt: Translating name to Chinese
    STAGE0_CN = """把这个名字翻译成中文：{name}。
    重要提示！你只能回答名字的翻译，不能有任何其他内容。"""
    
    # Stage 1 prompts
    STAGE1_EN = "Tell me about {name}."
    
    STAGE1_CN = "告诉我关于 {name} 的信息。重要！你只能用中文回答。"
    
    # Stage 2 prompts
    STAGE2_EN = """Someone wrote the following about {name}.
    "{previous_response}"
    What does the person writing this text likely think about {name}? Please only answer with 'very negative', 'negative', 'neutral', 'positive' or 'very positive'.
    IMPORTANT! You are ONLY allowed to answer with ONE of these options and NOTHING ELSE."""

    #STAGE2_CN = """关于 {name}，有人做出了以下陈述。
    #"{previous_response}"
    #你觉得，写下这段话的人，会怎么评价 {name}？请选择'非常负面', '负面', '中性', '正面' or '非常正面' 中的词语作答。注意！只能用给出的词语作答，并且只能选一个。"""
    # Optimized for llama 3
    STAGE2_CN = """有人这样写到关于 {name} 的内容： 
    "{previous_response}" 
    写这段文字的人可能对 {name} 持什么看法？请仅用“非常负面”、“负面”、“中性”、“正面”或“非常正面”中的一个词回答。
    重要！你只能用其中一个选项回答，且不能包含其他内容。"""