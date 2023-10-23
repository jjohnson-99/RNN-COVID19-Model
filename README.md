# RNN-COVID19-Model
Modeling the association between population mobility and new COVID-19 diagnoses in urban Wisconsin. This was a class project done in collaboration with Kevin Kristensen and Liban Mohamed. This repo contains the resulting pre-print as well a discussion of my contribution to the work. In particular, this discusses the data preparation and the neural networks used.

## To-do
- [ ] Rewrite models and experiment with the hyperparameters.
- [ ] Extend with newer data supplied to Google and the COVID-19 data repo.

## Overview and data preparation
This project takes using mobility data provided by Google at https://www.google.com/covid19/mobility/ and compares it to documented COVID-19 cases in Wisconsin, found at https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series.

The sources provide data for the entire United States. To reduce the complexity of the model and our interpretation, we decided to focus souly on Wisconsin. Upon looking at the Google mobility data, it was decided that data for many counties were missing so we elected to focus only on urban areas since these had more complete data. The data cleaning and concatinating is done by the data_prep.py code, resulting in the imputed_urban_wisconsin_data_with_counts.csv file. This is the only file that the neural_networks.ipynb notebook needs in order to run. The other source data are supplied for completion.

## The models
For the neural network models, we chose convolutional and recurrent neural networks to take advantage of the time-series nature of the data. In either method, the data are packaged into windows of specified input length, a potential offset, and label width. Each sample fed into the neural network therefore consists of some number of input days for which the model considers all five features, a number of offset days to ignore, then finally a label day for which the model predicts the number of new infections. The model is then applied to sliding windows of inputs.

The neural network models were created using the TensorFlow Keras library. The models were run using Mean Square Error loss functions and ADAM-Optimizer. The models are compared using Mean Absolute Error. We chose to use 16 counties chosen at random as test data, 4 counties as validation data, and 3 counties as test data. It would likely be preferred to split the training, validation, and testing data randomly but was foregone for ease of processing. These windows are created for each county, placed into batches of 32, then shuffled. The models are run over all batches for 20 epochs.

Either model runs over the samples in a slightly different way. For the convolution neural network, the model uses the previous 7 days of data for each prediction. It then slides over for a total of 24 days worth of predictions. We used a recurrent neural network called Long Short Term Memory (LSTM) which stacks layers, making a prediction for each input and maintains memory of each model used before.
