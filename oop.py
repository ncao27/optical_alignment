from BWExperiment import BWExperiment

# define angles
yaw1, yaw2, pitch1, pitch2 = 45, 135, 0, 0

bw = BWExperiment(yaw1, yaw2, pitch1, pitch2)
psf_data, psf_power = bw.compute_geo_psf()

print("PSF Power:", psf_power)