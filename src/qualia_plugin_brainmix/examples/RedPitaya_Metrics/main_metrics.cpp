// Copyright 2021 (c) Pierre-Emmanuel Novac <penovac@unice.fr>
// Université Côte d'Azur, CNRS, LEAT. All rights reserved.

#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <memory>
#include <sstream>
#include <vector>
#include <cmath>
#include <chrono>
#include <limits>

// RedPitaya GPIO API
#include "rp.h"

// Neural network headers
#include "NeuralNetwork.h"
#include "metrics.h"

// Read CSV into fixed-size float arrays
template<int N>
std::vector<std::array<float, N>> readInputsFromFile(const char *filename) {
	std::vector<std::array<float, N>> inputs;
	std::ifstream fin(filename);
	std::string linestr;
	while (std::getline(fin, linestr)) {
		std::istringstream linestrs(linestr);
		std::string floatstr;
		std::array<float, N> floats{};
		for (int i = 0; std::getline(linestrs, floatstr, ','); i++) {
			floats.at(i) = std::strtof(floatstr.c_str(), NULL);
		}
		inputs.push_back(floats);
	}
	return inputs;
}

// GPIO setup and control
bool setupGPIO() {
	if (rp_Init() != RP_OK) {
		std::cerr << "Failed to initialize RedPitaya GPIO API." << std::endl;
		return false;
	}
	rp_DpinSetDirection(RP_DIO0_P, RP_OUT);
	return true;
}

void setGPIO(bool high) {
	rp_DpinSetState(RP_DIO0_P, high ? RP_HIGH : RP_LOW);
}

// Run evaluation and collect metrics
template<size_t InputDims, size_t OutputDims>
void evaluate(const std::vector<std::array<float, InputDims>> &inputs, const std::vector<std::array<float, OutputDims>> &targets) {
	static NeuralNetwork nn{metrics};

	std::vector<double> latencies;
	double total_latency = 0.0;
	double max_latency = std::numeric_limits<double>::min();
	double min_latency = std::numeric_limits<double>::max();

	for (size_t i = 0; i < inputs.size(); i++) {
		auto start = std::chrono::steady_clock::now();

		nn.evaluate(inputs.at(i), targets.at(i));

		auto end = std::chrono::steady_clock::now();
		std::chrono::duration<double, std::micro> elapsed = end - start;
		double latency_us = elapsed.count();

		latencies.push_back(latency_us);
		total_latency += latency_us;
		if (latency_us > max_latency) max_latency = latency_us;
		if (latency_us < min_latency) min_latency = latency_us;
	}

	auto metrics_result = nn.getMetricsResult();

	for (size_t i = 0; i < metrics.size() && i < metrics_result.size(); i++) {
		std::cerr << metrics[i]->name() << "=" << metrics_result[i] << std::endl;
	}

	std::cerr << "Latency (µs): min = " << min_latency
	          << ", max = " << max_latency
	          << ", avg = " << (total_latency / latencies.size()) << std::endl;
}

int main(int argc, const char *argv[]) {
	if (argc != 3) {
		std::cerr << "Usage: " << argv[0] << " testX.csv testY.csv" << std::endl;
		return 1;
	}

	if (!setupGPIO()) return 1;

	auto inputs = readInputsFromFile<MODEL_INPUT_DIMS>(argv[1]);
	auto labels = readInputsFromFile<MODEL_OUTPUT_SAMPLES>(argv[2]);

	setGPIO(true); // Signal start to Otii
	evaluate(inputs, labels);
	setGPIO(false); // Signal stop to Otii

	rp_Release(); // Clean up GPIO API

	return 0;
}
