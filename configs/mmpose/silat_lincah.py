# Silat Lincah Pose Estimation Configuration
# Based on MMPose framework

_base_ = [
    '../_base_/default_runtime.py',
    '../_base_/data/coco_pose.py'
]

# Model configuration for Silat Lincah
model = dict(
    type='TopDown',
    pretrained='https://download.openmmlab.com/mmpose/pretrain_models/hrnet_w48-8ef0771d.pth',
    backbone=dict(
        type='HRNet',
        in_channels=3,
        extra=dict(
            stage1=dict(
                num_modules=1,
                num_branches=1,
                block='BOTTLENECK',
                num_blocks=(4,),
                num_channels=(64,)),
            stage2=dict(
                num_modules=1,
                num_branches=2,
                block='BASIC',
                num_blocks=(4, 4),
                num_channels=(48, 96)),
            stage3=dict(
                num_modules=4,
                num_branches=3,
                block='BASIC',
                num_blocks=(4, 4, 4),
                num_channels=(48, 96, 192)),
            stage4=dict(
                num_modules=3,
                num_branches=4,
                block='BASIC',
                num_blocks=(4, 4, 4, 4),
                num_channels=(48, 96, 192, 384)))),
    keypoint_head=dict(
        type='TopDownSimpleHead',
        in_channels=48,
        out_channels=17,  # Standard COCO keypoints adapted for Silat Lincah
        num_deconv_layers=0,
        extra=dict(final_conv_kernel=1, ),
        loss_keypoint=dict(type='JointsMSELoss', use_target_weight=True)),
    train_cfg=dict(),
    test_cfg=dict(
        flip_test=True,
        post_process='default',
        shift_heatmap=True,
        modulate_kernel=11))

# Silat Lincah specific keypoint configuration
silat_lincah_keypoints = [
    'nose',           # 0
    'left_eye',       # 1
    'right_eye',      # 2
    'left_ear',       # 3
    'right_ear',      # 4
    'left_shoulder',  # 5
    'right_shoulder', # 6
    'left_elbow',     # 7
    'right_elbow',    # 8
    'left_wrist',     # 9
    'right_wrist',    # 10
    'left_hip',       # 11
    'right_hip',      # 12
    'left_knee',      # 13
    'right_knee',     # 14
    'left_ankle',     # 15
    'right_ankle'     # 16
]

# Silat Lincah skeleton connections
silat_lincah_skeleton = [
    [16, 14], [14, 12], [17, 15], [15, 13], [12, 13],
    [6, 12], [7, 13], [6, 7], [6, 8], [7, 9],
    [8, 10], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]
]

# Dataset configuration for Silat Lincah
dataset_type = 'CocoDataset'
data_root = 'data/'

# Training pipeline
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='TopDownGetBboxCenterScale', padding=1.25),
    dict(type='TopDownRandomShiftBboxCenter', shift_factor=0.16, prob=0.3),
    dict(type='TopDownRandomFlip', flip_prob=0.5),
    dict(
        type='TopDownHalfBodyTransform',
        num_joints_half_body=8,
        prob_half_body=0.3),
    dict(
        type='TopDownGetRandomScaleRotation', rot_factor=40, scale_factor=0.5),
    dict(type='TopDownAffine'),
    dict(type='ToTensor'),
    dict(
        type='NormalizeTensor',
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]),
    dict(
        type='TopDownGenerateTarget',
        sigma=2,
        encoding='MSRA'),
    dict(
        type='Collect',
        keys=['img', 'target', 'target_weight'],
        meta_keys=[
            'image_file', 'joints_3d', 'joints_3d_visible', 'center', 'scale',
            'rotation', 'bbox_score', 'flip_pairs'
        ]),
]

# Validation pipeline
val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='TopDownGetBboxCenterScale', padding=1.25),
    dict(type='TopDownAffine'),
    dict(type='ToTensor'),
    dict(
        type='NormalizeTensor',
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]),
    dict(
        type='Collect',
        keys=['img'],
        meta_keys=[
            'image_file', 'center', 'scale', 'rotation', 'bbox_score',
            'flip_pairs'
        ]),
]

# Test pipeline
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='TopDownGetBboxCenterScale', padding=1.25),
    dict(type='TopDownAffine'),
    dict(type='ToTensor'),
    dict(
        type='NormalizeTensor',
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]),
    dict(
        type='Collect',
        keys=['img'],
        meta_keys=[
            'image_file', 'center', 'scale', 'rotation', 'bbox_score',
            'flip_pairs'
        ]),
]

# Training dataset
train_dataset = dict(
    type=dataset_type,
    ann_file=f'{data_root}annotations/silat_lincah_train.json',
    img_prefix=f'{data_root}processed/train/',
    data_cfg=dict(
        image_size=[256, 256],
        heatmap_size=[64, 64],
        num_joints=17,
        dataset_channel=silat_lincah_keypoints,
        joint_channel=silat_lincah_skeleton),
    pipeline=train_pipeline,
    dataset_info=dict(dataset_name='SilatLincah'))

# Validation dataset
val_dataset = dict(
    type=dataset_type,
    ann_file=f'{data_root}annotations/silat_lincah_val.json',
    img_prefix=f'{data_root}processed/val/',
    data_cfg=dict(
        image_size=[256, 256],
        heatmap_size=[64, 64],
        num_joints=17,
        dataset_channel=silat_lincah_keypoints,
        joint_channel=silat_lincah_skeleton),
    pipeline=val_pipeline,
    dataset_info=dict(dataset_name='SilatLincah'))

# Test dataset
test_dataset = dict(
    type=dataset_type,
    ann_file=f'{data_root}annotations/silat_lincah_test.json',
    img_prefix=f'{data_root}processed/test/',
    data_cfg=dict(
        image_size=[256, 256],
        heatmap_size=[64, 64],
        num_joints=17,
        dataset_channel=silat_lincah_keypoints,
        joint_channel=silat_lincah_skeleton),
    pipeline=test_pipeline,
    dataset_info=dict(dataset_name='SilatLincah'))

# Data loading
data = dict(
    samples_per_gpu=32,
    workers_per_gpu=2,
    train=train_dataset,
    val=val_dataset,
    test=test_dataset)

# Training configuration
optimizer = dict(type='Adam', lr=0.001)
optimizer_config = dict(grad_clip=None)
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[170, 200])
total_epochs = 210

# Evaluation
evaluation = dict(interval=10, metric='PCKh', save_best='PCKh')

# Checkpoint saving
checkpoint_config = dict(interval=10)
log_config = dict(
    interval=50,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])

# Runtime configuration
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './work_dirs/silat_lincah_pose'
load_from = None
resume_from = None
workflow = [('train', 1)]
