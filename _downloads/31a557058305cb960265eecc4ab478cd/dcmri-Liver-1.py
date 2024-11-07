import matplotlib.pyplot as plt
import dcmri as dc
#
# Use `fake_liver` to generate synthetic test data:
#
time, aif, vif, roi, gt = dc.fake_liver()
#
# Build a tissue model and set the constants to match the experimental
# conditions of the synthetic test data:
#
model = dc.Liver(
    aif = aif,
    dt = time[1],
    agent = 'gadoxetate',
    field_strength = 3.0,
    TR = 0.005,
    FA = 15,
    n0 = 10,
    kinetics = '1I-IC-D',
    R10 = 1/dc.T1(3.0,'liver'),
    R10a = 1/dc.T1(3.0, 'blood'),
)
#
# Train the model on the ROI data:
#
model.train(time, roi)
#
# Plot the reconstructed signals (left) and concentrations (right) and
# compare the concentrations against the noise-free ground truth:
#
model.plot(time, roi, ref=gt)
