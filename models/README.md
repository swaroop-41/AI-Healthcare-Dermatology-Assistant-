# Model Directory

Place your trained ResNet18 model file here:

```
models/skin_multiclass.pth
```

## Training the Model

To train a new model, use the training script:

```bash
cd training/dermatology
python train_skin_model.py --data_path /path/to/ISIC_dataset --epochs 50 --batch_size 32
```

## Expected Model Format

- **Architecture**: ResNet18
- **Input**: 224x224 RGB images
- **Output**: 8 classes (AK, BCC, BKL, DF, MEL, NV, SCC, VASC)
- **File format**: PyTorch state_dict (.pth)

## Model Performance

The provided model (if available) achieves:
- **Accuracy**: 86% on ISIC validation set
- **Training Dataset**: ISIC Archive
- **Classes**: 8 skin conditions

## Using a Custom Model

If you have your own trained model, ensure it:
1. Uses ResNet18 architecture
2. Has 8 output classes matching our class order
3. Was saved using `torch.save(model.state_dict(), path)`

## Notes

- The application will work without a trained model, but predictions will be random
- For production use, always use a properly trained and validated model
- Consider model versioning for tracking performance over time
