################Deformable Detr###################
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/deformable_detr/FD/deformable_detr_FD_load.py --work-dir ./experiments/FD_load_deform --auto-scale-lr

###################DINO############################
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/dino/FD/dino_detr_FD_load.py --work-dir ./experiments/FD_load_dino --auto-scale-lr

##############DIFF DETR############################
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/DiffusionDet/configs/FD/diff_detr_FD_load.py --work-dir ./experiments/FD_load_diff --auto-scale-lr

###################GLIP EXPERIMENTS################
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/glip/FD/glip_FD_baseline.py --work-dir ./experiments/FD_glip --auto-scale-lr
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/glip/FD/glip_FD_BCG.py --work-dir ./experiments/FD_BCG_glip --auto-scale-lr

####################Grounding DINO Baseline########
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/grounding_dino/FD/grounding_FD_baseline.py --work-dir ./experiments/FD_gdino --auto-scale-lr
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/grounding_dino/FD/grounding_FD_BCG.py --work-dir ./experiments/FD_BCG_gdino --auto-scale-lr

#####################FD-SOS########################
CUDA_VISIBLE_DEVICES=0 python tools/train.py configs/FD-SOS/grounding_FD_BCG_teeth_specific.py --work-dir ./experiments/FD_BCG_SOS --auto-scale-lr
