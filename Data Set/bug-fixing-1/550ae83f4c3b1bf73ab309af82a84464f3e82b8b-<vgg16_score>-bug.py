

def vgg16_score(input, numclass, workspace_default=1024):
    conv5_1 = mx.symbol.Convolution(data=input, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=workspace_default, name='conv5_1')
    relu5_1 = mx.symbol.Activation(data=conv5_1, act_type='relu', name='relu5_1')
    conv5_2 = mx.symbol.Convolution(data=relu5_1, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=workspace_default, name='conv5_2')
    relu5_2 = mx.symbol.Activation(data=conv5_2, act_type='relu', name='conv1_2')
    conv5_3 = mx.symbol.Convolution(data=relu5_2, kernel=(3, 3), pad=(1, 1), num_filter=512, workspace=workspace_default, name='conv5_3')
    relu5_3 = mx.symbol.Activation(data=conv5_3, act_type='relu', name='relu5_3')
    pool5 = mx.symbol.Pooling(data=relu5_3, pool_type='max', kernel=(2, 2), stride=(2, 2), name='pool5')
    fc6 = mx.symbol.Convolution(data=pool5, kernel=(7, 7), num_filter=4096, workspace=workspace_default, name='fc6')
    relu6 = mx.symbol.Activation(data=fc6, act_type='relu', name='relu6')
    drop6 = mx.symbol.Dropout(data=relu6, p=0.5, name='drop6')
    fc7 = mx.symbol.Convolution(data=drop6, kernel=(1, 1), num_filter=4096, workspace=workspace_default, name='fc7')
    relu7 = mx.symbol.Activation(data=fc7, act_type='relu', name='relu7')
    drop7 = mx.symbol.Dropout(data=relu7, p=0.5, name='drop7')
    score = mx.symbol.Convolution(data=drop7, kernel=(1, 1), num_filter=numclass, workspace=workspace_default, name='score')
    return score
