from quadoa import *
import numpy as np

class BWExperiment:

    core: QuadoaCore = QuadoaCore()

    def __init__(self, yaw1, yaw2, pitch1, pitch2, qbase_folder, material_file, model_folder, model_file):
        self.yaw1 = yaw1
        self.yaw2 = yaw2
        self.pitch1 = pitch1
        self.pitch2 = pitch2
        self.qbase_folder = qbase_folder
        self.material_file = material_file
        self.model_folder = model_folder
        self.model_file = model_file

    def set_angles(self, yaw1 = None, yaw2 = None, pitch1 = None, pitch2 = None):

        if yaw1 is not None: self.yaw1 = yaw1
        if yaw2 is not None: self.yaw2 = yaw2
        if pitch1 is not None: self.pitch1 = pitch1
        if pitch2 is not None: self.pitch2 = pitch2

        # Apply angles to the model
        self.core.setOpticalSystemParamByIndexD(6, 10, self.yaw1)
        self.core.setOpticalSystemParamByIndexD(9, 10, self.yaw2)
        self.core.setOpticalSystemParamByIndexD(6, 11, self.pitch1)
        self.core.setOpticalSystemParamByIndexD(9, 11, self.pitch2)

    def compute_geo_psf(self):

        """
        Function:
            Perform one forward pass of a ray-trace simulation.

        Args:
            None. utilizes the angular values that the user sets

        Returns:
            psf_data: numpy matrix that represents the psf on the image plane calculated through geometric ray-tracing
            psf_power: the float returned when we sum up all the values on the image plane
        """


        core: QuadoaCore = QuadoaCore()

        QuadoaBaseFolder = "E:/Program Files/Quadoa"
        # load material catalogs
        core.loadMaterialFile("E:/Program Files/Quadoa/glass/CDGM.glas")

        # load the lens file
        ModelFolder = "C:/Users/Nathan Cao/OneDrive/Desktop/quadoa_projects"
        core.loadModelFile(ModelFolder + "/beam_walking.optx")

        core.applyChangesAndInitModel()

        data = core.getGeoPSF(0, 0, 0, 17)

        # this is just the numpy array version of the PSF
        psf_data = np.array(data, copy=False)

        # compute the total power of the psf (because it's discrete we just use the sum function
        psf_power = np.sum(psf_data)

        return psf_data, psf_power

    def get_angles(self):
        return self.yaw1, self.yaw2, self.pitch1, self.pitch2



