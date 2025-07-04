# Project Description

A series of python scripts to perform analysis on the imaging plane of a Quadoa ray-tracing simulation. 

**Note to reader:** Quadoa can be acquired through proof of enrollment at an educational institution.

## 1. intensity_data

The file named intensity_data contains the contents generated through forward simulations. `two_deg` contains simulation results generated through simulations involving two degrees of freedom (yaw1 and yaw2). `four_deg` contains simulation results generated through simulations involving four degrees of freedom (yaw1, yaw2, pitch1, pitch2).

## 2. hyperterminal.py

Contains the code necessary to interface with OptoSigma piezoelectric motors.

## 3. intensity_analysis_two.py

Contains the code necessary to analyze the data generated through forward simulations involving only two degrees (yaw1 and yaw2) of freedom.

## 4. intensity_analysis_four.py

Contains the code necessary to analyze the data generated through forward simulations involving all four degrees (yaw1, yaw2, pitch1, pitch2) of freedom.

## 5. psf_parallel.py

Contains the code necessary to run parallel forward simulations on a multicore CPU using joblib.

## 6. psf_nested.py

Contains the code necessary to run non-parallelized forward simulations.

## 7. psf_test.py

Contains the code necessary to analyze the psf spot size on the imaging plane of a single forward simulation pass.

## 8. spot_diagram.py

Contains the code necessary to plot the spot diagram on the imaging plane.

## 9. beam_walking.optx

Contains the specifications for the beam walking setup generated using the Quadoa ray-tracing software.
