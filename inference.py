from mmdet.evaluation.metrics.coco_metric import CocoMetric
import os
from mmdet.apis import DetInferencer

root_dir = r'./experiments'
batch_size = 8

# 配置文件映射
config_mapping = {
    'FD_diff': 'configs/DiffusionDet/configs/diffusiondet_swin_fpn_500.py',
    'FD_load_deform': 'configs/deformable_detr/deformable-detr_r50_16xb2-50e_coco.py',
    'FD_load_dino': 'configs/dino/dino-4scale_r50_8xb2-12e_coco.py',
    'FD_load_diff': 'configs/DiffusionDet/configs/diffusiondet_swin_fpn_500.py',
    'FD_glip': 'configs/glip/glip_atss_swin-t_a_fpn_dyhead_16xb2_ms-2x_funtune_coco.py',
    'FD_gdino': 'configs/grounding_dino/grounding_dino_swin-t_finetune_16xb2_1x_coco.py',
    'FD_BCG_glip': 'configs/glip/glip_atss_swin-t_a_fpn_dyhead_16xb2_ms-2x_funtune_coco.py',
    'FD_BCG_gdino': 'configs/grounding_dino/grounding_dino_swin-t_finetune_16xb2_1x_coco.py',
    'FD_BCG_SOS': 'configs/FD-SOS/grounding_FD_BCG_teeth_specific.py',
}

experiments_to_infer = [
    f"FD_diff", #

    f"FD_load_deform", #
    f"FD_load_dino", #
    f"FD_load_diff", #

    f"FD_glip", #
    f"FD_gdino", #

    f"FD_BCG_glip",  #
    f"FD_BCG_gdino", #
    f"FD_BCG_SOS", #

]

class_name_1 = (
    "posterior teeth",
    "anterior teeth",
    "anterior teeth No FD",
    "anterior teeth FD",
)

coco_1 = CocoMetric(
    ann_file=r'data/v1/40_FD_BCG_test.json'
    , classwise=True)

coco_1.cat_ids = coco_1._coco_api.get_cat_ids(cat_names=list(class_name_1))

coco_1.img_ids = coco_1._coco_api.get_img_ids()

test_image_ids = coco_1.img_ids
coco_images = []
coco_annotations = []
image_id, annotation_id = 1, 1
all_list = []
for img_idx in test_image_ids:
    image_meta_info = coco_1._coco_api.loadImgs(img_idx)
    image_file = image_meta_info[0]['file_name']
    all_list.append(os.path.join('data/v1/images_all', image_file))

for _work_dir in experiments_to_infer:
    work_dir = os.path.join(root_dir, _work_dir)
    if os.path.exists(work_dir):
        out_work_dir = work_dir.split('/')[-1]

        # 查找最佳权重文件
        best_checkpoint = [i for i in os.listdir(work_dir) if i.startswith('best_')][-1]
        
        # 从配置映射中获取配置文件路径
        if _work_dir in config_mapping:
            config_path = config_mapping[_work_dir]
        else:
            print(f'No config mapping found for {_work_dir}, skipping...')
            continue
            
        # 检查配置文件是否存在
        if not os.path.exists(config_path):
            print(f'Config file {config_path} does not exist, skipping {_work_dir}...')
            continue

        # Setup a checkpoint file to load
        checkpoint = os.path.join(work_dir, best_checkpoint)

        # Initialize the DetInferencer
        inferencer = DetInferencer(model=config_path, weights=checkpoint, device='cuda:0')

        if 'BCG' in out_work_dir:
            texts = "posterior teeth. anterior teeth. anterior teeth No FD. anterior teeth FD"
        else:
            texts = "anterior teeth No FD. anterior teeth FD"

        _ = inferencer(all_list,
                       texts=texts,
                       custom_entities=True,
                       out_dir=f"predictions/{out_work_dir}/", no_save_pred=False, batch_size=batch_size,
                       no_save_vis=True)
    else:
        print(f'Path {work_dir} is not existing')
