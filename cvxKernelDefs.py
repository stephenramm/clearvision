# Standard OpenVX kernel definition dictionary
#
# Each entry is in the form:
# 'kernel name' , 'node function name - if any', 'VX_KERNEL_ enumeration', parameter_list, match_conditions)
# Where match_condition is a string to be interpreted by the match condition parser
#
# Each parameter list entry is in the form:
# ('parameter name', direction, state, type, requirement, default)
# Where direction is kpInput, kpOutput or 'VX_BIDIRECTIONAL'
#       state is kpRequired, kpOptional or kpImmutable
#       type is a vx_xxx type (in quotes)
#       requirement is a string to be interpreted by the requirement parser

# Note on requirements and match conditions.
# Requirement applies only to the associated parameter, match condition applies to all of the kernel.
# When choosing values for a virtual object, each 'OR' clause in a requirement must be tested in turn against the
# match conditions, i.e. the first values are tried first, for example the vxAddNode out parameter is always going
# to be an S16 image unless it is explicitly set to U8.

# Constants for indexing the structures:

kpInput = 'VX_INPUT'
kpOutput = 'VX_OUTPUT'
kpBidirectional = 'VX_BIDIRECTIONAL'
kpRequired = 'VX_PARAMETER_STATE_REQUIRED'
kpOptional = 'VX_PARAMETER_STATE_OPTIONAL'
kpImmutable = 'VX_PARAMETER_STATE_IMMUTABLE'

# TODO:
# Deafult values for parameters?

from cvxDataDefs import *

class ParameterDef(object):
    """
    class to manage a kernel parameter
    """
    def __init__(self, pname, pdir, pstate, ptype, preq):
        self.pname = pname      # parameter name
        self.pdir = pdir        # parameter direction
        self.pstate = pstate    # parameter state
        self.ptype = ptype      # parameter type
        self.preq = preq        # parameter requirements for validation

    def __str__(self):
        return "{pname='%s', pdir='%s', pstate='%s', ptype='%s', preq='%s'}"%(self.pname, self.pdir, self.pstate, self.ptype, self.preq)

class KernelDef(object):
    """
    class to manage a dictionary of kernel definitions
    """
    kernelDict = dict()

    def __init__(self, kname, fname, kenum, params, kreq):
        self.kname = kname      # kernel name
        self.fname = fname   # The name of the node creation function, used in code writing
        self.kenum = kenum      # The kernel enumeration label (may not be required)
        self.params = params    # a list of parameter definition objects
        self.kreq   = kreq      # requirements for validation
        KernelDef.kernelDict[kname] = self

    @staticmethod
    def get(name):
        """
        Retrieve the kernel definition for the given name
        """
        return KernelDef.kernelDict.get(name)

    @staticmethod
    def keys():
        """
        Retrieve the list of kernel names
        """
        return list(KernelDef.kernelDict.keys())

    @staticmethod
    def values():
        """
        Retrieve the list of kernel definitions
        """
        return list(KernelDef.kernelDict.values())

    @staticmethod
    def items():
        """
        Retrieve the list of (kernel name, kernel definition) pairs
        """
        return list(KernelDef.kernelDict.items())

KernelDef('org.khronos.openvx.color_convert', 'vxColorConvertNode', 'VX_KERNEL_COLOR_CONVERT',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, '')
    ], 'output.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.channel_extract', 'vxChannelExtractNode', 'VX_KERNEL_CHANNEL_EXTRACT',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, ''),
    ParameterDef('channel', kpInput, kpImmutable, 'vx_channel_e', ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.channel_combine', 'vxChannelCombineNode', 'VX_KERNEL_CHANNEL_COMBINE', 
    [
    ParameterDef('plane0', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('plane1', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('plane2', kpInput, kpOptional, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('plane3', kpInput, kpOptional, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, '')       
    ], 'output.VX_IMAGE_WIDTH is plane0.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is plane0.VX_IMAGE_HEIGHT and '
       'plane0 is plane1 and plane1 is plane2 and plane2 is plane3')

KernelDef('org.khronos.openvx.sobel_3x3', 'vxSobel3x3Node', 'VX_KERNEL_SOBEL_3x3',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('output_x', kpOutput, kpOptional, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16'),
    ParameterDef('output_y', kpOutput, kpOptional, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16')        
    ], 'output_x is output_y and output_x.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and output_x.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.magnitude', 'vxMagnitudeNode', 'VX_KERNEL_MAGNITUDE', 
    [
    ParameterDef('grad_x', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16'),
    ParameterDef('grad_y', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16'),
    ParameterDef('mag', kpOutput, kpRequired, s_vx_image, 'mag.VX_IMAGE_FORMAT is VX_DF_IMAGE_S16')        
    ], 'mag is grad_x and mag is grad_y')

KernelDef('org.khronos.openvx.phase', 'vxPhaseNode', 'VX_KERNEL_PHASE',
    [
    ParameterDef('grad_x', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16'),
    ParameterDef('grad_y', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16'),
    ParameterDef('orientation', kpOutput, kpRequired, s_vx_image, 'orientation.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')        
    ], 'orientation.VX_IMAGE_WIDTH is grad_x.VX_IMAGE_WIDTH and orientation.VX_IMAGE_HEIGHT is grad_x.VX_IMAGE_HEIGHT and grad_x is grad_y')

KernelDef('org.khronos.openvx.scale_image', 'vxScaleImageNode', 'VX_KERNEL_SCALE_IMAGE',
    [
    ParameterDef(s_src, kpInput, kpRequired, s_vx_image, ''),
    ParameterDef(s_dst, kpOutput, kpRequired, s_vx_image, ''),
    ParameterDef('type', kpInput, kpImmutable, 'vx_interpolation_type_e', '')
    ], 'dst.VX_IMAGE_FORMAT is src.VX_IMAGE_FORMAT')

KernelDef('org.khronos.openvx.table_lookup', 'vxTableLookupNode', 'VX_KERNEL_TABLE_LOOKUP',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_S16, VX_DF_IMAGE_U8]'),
    ParameterDef('lut', kpInput, kpRequired, s_vx_lut, 'VX_LUT_TYPE in [VX_TYPE_UINT8, VX_TYPE_INT16]'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_S16, VX_DF_IMAGE_U8]')
    ], 'output is input')

KernelDef('org.khronos.openvx.histogram', 'vxHistogramNode', 'VX_KERNEL_HISTOGRAM',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('distribution', kpOutput, kpRequired, s_vx_distribution, '')
    ], '')

KernelDef('org.khronos.openvx.equalize_histogram', 'vxEqualizeHistNode', 'VX_KERNEL_EQUALIZE_HISTOGRAM',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ], 'output is input')

KernelDef('org.khronos.openvx.absdiff', 'vxAbsDiffNode', 'VX_KERNEL_ABSDIFF',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_S16, VX_DF_IMAGE_U8]'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_S16, VX_DF_IMAGE_U8]'),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_S16, VX_DF_IMAGE_U8]')
    ], '') #TODO: need some complicated condition here since output can only be u8 if both inputs are u8

KernelDef('org.khronos.openvx.mean_stddev', 'vxMeanStdDevNode', 'VX_KERNEL_MEAN_STDDEV',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('mean', kpOutput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('stddev', kpOutput, kpOptional, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32')
    ], '')

KernelDef('org.khronos.openvx.threshold', 'vxThresholdNode', 'VX_KERNEL_THRESHOLD',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_S16, VX_DF_IMAGE_U8]'),
    ParameterDef('thresh', kpInput, kpRequired, s_vx_threshold, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], '')

KernelDef('org.khronos.openvx.integral_image', 'vxIntegralIMageNode', 'VX_KERNEL_INTEGRAL_IMAGE',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U32')
    ], '')

KernelDef('org.khronos.openvx.dilate_3x3', 'vxDilate3x3Node', 'VX_KERNEL_DILATE_3x3',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.erode_3x3', 'vxErode3x3Node', 'VX_KERNEL_ERODE_3x3',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')


KernelDef('org.khronos.openvx.median_3x3', 'vxMedian3x3Node', 'VX_KERNEL_MEDIAN_3x3',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')


KernelDef('org.khronos.openvx.box_3x3', 'vxBox3x3Node', 'VX_KERNEL_BOX_3x3',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')


KernelDef('org.khronos.openvx.gaussian_3x3', 'vxGaussian3x3Node', 'VX_KERNEL_GAUSSIAN_3x3',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.custom_convolution', 'vxConvolveNode', 'VX_KERNEL_CUSTOM_CONVOLUTION',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('conv', kpInput, kpRequired, s_vx_convolution, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]')
    ], 'output.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is input.vx_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.gaussian_pyramid', 'vxGaussianPyramidNode', 'VX_KERNEL_GAUSSIAN_PYRAMID',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('gaussian', kpOutput, kpRequired, s_vx_pyramid, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], '')

KernelDef('org.khronos.openvx.accumulate', 'vxAccumulateImageNode', 'VX_KERNEL_ACCUMULATE',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_accum, kpBidirectional, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16')
    ], 'accum.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and accum.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.accumulate_weighted', 'vxAccumulateWeightedImageNode', 'VX_KERNEL_ACCUMULATE_WEIGHTED',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('alpha', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32 and 0.0 <=  $value <= 1.0'),
    ParameterDef(s_accum, kpBidirectional, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'accum.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and accum.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.accumulate_square', 'vxAccumulateSquareImageNode', 'VX_KERNEL_ACCUMULATE_SQUARE',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('shift', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_UINT32 and 0 <=  $value <= 15'),
    ParameterDef(s_accum, kpBidirectional, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16')
    ], 'accum.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and accum.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.minmaxloc', 'vxMinMaxLocNOde', 'VX_KERNEL_MINMAXLOC',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef('minVal', kpOutput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE in [VX_TYPE_UINT8, VX_TYPE_INT16]'),
    ParameterDef('maxVal', kpOutput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE in [VX_TYPE_UINT8, VX_TYPE_INT16]'),
    ParameterDef('minloc', kpOutput, kpOptional, s_vx_array, 'VX_ARRAY_ITEM_TYPE is VX_TYPE_COORDINATES2D'),
    ParameterDef('maxloc', kpOutput, kpOptional, s_vx_array, 'VX_ARRAY_ITEM_TYPE is VX_TYPE_COORDINATES2D'),
    ParameterDef('minCount', kpOutput, kpOptional, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_SIZE'),
    ParameterDef('maxCount', kpOutput, kpOptional, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_SIZE')        
    ], '')

KernelDef('org.khronos.openvx.convertdepth', '', 'VX_KERNEL_CONVERTDEPTH',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, ''),
    ParameterDef(s_policy, kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef('shift', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_INT32')
    ], 'output.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')


KernelDef('org.khronos.openvx.canny_edge_detector', 'vxCannyEdgeDetectorNode', 'VX_KERNEL_CANNY_EDGE_DETECTOR',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, ''),
    ParameterDef('hyst', kpInput, kpRequired, s_vx_threshold, ''),
    ParameterDef('gradient_size', kpInput, kpImmutable, s_vx_uint32, ''),
    ParameterDef('norm_type', kpInput, kpImmutable, 'vx_norm_type_e', ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, '')
    ], '')

KernelDef('org.khronos.openvx.and', 'vxAndNode', 'VX_KERNEL_AND',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'out is in1 and out is in2')

KernelDef('org.khronos.openvx.or', 'vxOrNode', 'VX_KERNEL_OR',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'out is in1 and out is in2')

KernelDef('org.khronos.openvx.xor', 'vxXorNode', 'VX_KERNEL_XOR',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'out is in1 and out is in2')

KernelDef('org.khronos.openvx.not', 'vxNotNode', 'VX_KERNEL_NOT',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.multiply', '', 'VX_KERNEL_MULTIPLY',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef('scale', kpInput, kpRequired,s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('overflow_policy', kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef('rounding_policy', kpInput, kpImmutable, 'vx_round_policy_e', ''),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]')
    ],
    '(out.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 and '
    'in1.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 and '
    'in2.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 or '
    'out.VX_IMAGE_FORMAT is VX_DF_IMAGE_S16) and '
    'out.VX_IMAGE_WIDTH is in1.VX_IMAGE_WIDTH and '
    'out.VX_IMAGE_HEIGHT is in1.VX_IMAGE_HEIGHT and '
    'out.VX_IMAGE_WIDTH is in2.VX_IMAGE_WIDTH and '
    'out.VX_IMAGE_HEIGHT is in2.VX_IMAGE_HEIGHT')


KernelDef('org.khronos.openvx.add', 'vxAddNode', 'VX_KERNEL_ADD',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef(s_policy, kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]')
    ],
    '(out.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 and '
    'in1.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 and '
    'in2.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 or '
    'out.VX_IMAGE_FORMAT is VX_DF_IMAGE_S16) and '
    'out.VX_IMAGE_WIDTH is in1.VX_IMAGE_WIDTH and '
    'out.VX_IMAGE_HEIGHT is in1.VX_IMAGE_HEIGHT and '
    'out.VX_IMAGE_WIDTH is in2.VX_IMAGE_WIDTH and '
    'out.VX_IMAGE_HEIGHT is in2.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.subtract', 'vxSubtractNode', 'VX_KERNEL_SUBTRACT',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef(s_policy, kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]')
    ],
    '(out.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 and '
    'in1.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 and '
    'in2.VX_IMAGE_FORMAT is VX_DF_IMAGE_U8 or '
    'out.VX_IMAGE_FORMAT is VX_DF_IMAGE_S16) and '
    'out.VX_IMAGE_WIDTH is in1.VX_IMAGE_WIDTH and '
    'out.VX_IMAGE_HEIGHT is in1.VX_IMAGE_HEIGHT and '
    'out.VX_IMAGE_WIDTH is in2.VX_IMAGE_WIDTH and '
    'out.VX_IMAGE_HEIGHT is in2.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.warp_affine', 'vxWarpAffineNode', 'VX_KERNEL_WARP_AFFINE' , 
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('matrix', kpInput, kpRequired, s_vx_matrix, 'VX_MATRIX_COLUMNS is 2 and VX_MATRIX_ROWS is 3 and VX_MATRIX_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('type', kpInput, kpImmutable, 'vx_interpolation_type_e', ' $value  is not VX_INTERPOLATION_AREA'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.warp_perspective', 'vxWarpPerspectiveNode', 'VX_KERNEL_WARP_PERSPECTIVE',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('matrix', kpInput, kpRequired, s_vx_matrix, 'VX_MATRIX_COLUMNS is 3 and VX_MATRIX_ROWS is 3 and VX_MATRIX_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('type', kpInput, kpImmutable, 'vx_interpolation_type_e', ' $value ! is  VX_INTERPOLATION_AREA'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.harris_corners', 'vxHarrisCornersNode', 'VX_KERNEL_HARRIS_CORNERS',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('strength_thresh', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('min_distance', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('sensitivity', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('gradient_size', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('block_size', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('corners', kpOutput, kpRequired, s_vx_array, 'VX_ARRAY_ITEM_TYPE is VX_TYPE_KEYPOINT'),
    ParameterDef('num_corners', kpOutput, kpOptional, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_SIZE')
    ], '')

KernelDef('org.khronos.openvx.fast_corners', 'vxFastCornersNode', 'VX_KERNEL_FAST_CORNERS',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('strength_thresh', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('nonmax_suppression', kpInput, kpImmutable, 'vx_bool', ''),
    ParameterDef('corners', kpOutput, kpRequired, s_vx_array, 'VX_ARRAY_ITEM_TYPE is VX_TYPE_KEYPOINT'),
    ParameterDef('num_corners', kpOutput, kpOptional, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_SIZE')        
    ], '')

KernelDef('org.khronos.openvx.optical_flow_pyr_lk', 'vxOpticalFlowPyrLKNode', 'VX_KERNEL_OPTICAL_FLOW_PYR_LK',
    [
    ParameterDef('old_images', kpInput, kpRequired, s_vx_pyramid, 'VX_PYRAMID_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('new_images', kpInput, kpRequired, s_vx_pyramid, 'VX_PYRAMID_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('old_points', kpInput, kpRequired, s_vx_array, 'VX_ARRAY_ITEM_TYPE is VX_TYPE_KEYPOINT'),
    ParameterDef('new_points_estimates', kpInput, kpRequired, s_vx_array, 'VX_ARRAY_ITEM_TYPE is VX_TYPE_KEYPOINT'),
    ParameterDef('new_points', kpOutput, kpRequired, s_vx_array, 'VX_ARRAY_ITEM_TYPE is VX_TYPE_KEYPOINT'),
    ParameterDef('termination', kpInput, kpImmutable, 'vx_termination_criteria_e', ''),
    ParameterDef('epsilon', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('num_iterations', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_UINT32'),
    ParameterDef('use_initial_estimate', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_BOOL'),
    ParameterDef('window_dimension', kpInput, kpImmutable, s_vx_size, '')
    ], '')

KernelDef('org.khronos.openvx.remap', 'vxRemapNode', 'VX_KERNEL_REMAP',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('table', kpInput, kpRequired, s_vx_remap, ''),
    ParameterDef(s_policy, kpInput, kpImmutable, 'vx_interpolation_type_e', ' $value  is not VX_INTERPOLATION_TYPE_AREA'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.halfscale_gaussian', 'vxHalfScaleGaussianNode', 'VX_KERNEL_HALFSCALE_GAUSSIAN',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'), 
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'), 
    ParameterDef('kernel_size', kpInput, kpImmutable, s_vx_int32, ' $value > 0')
    ], 'output.VX_IMAGE_WIDTH is (input.VX_IMAGE_WIDTH + 1)/2 and output.VX_IMAGE_HEIGHT is (input.VX_IMAGE_HEIGHT + 1)/2')

KernelDef('org.khronos.openvx.laplacian_pyramid', 'vxLaplacianPyramidNode', 'VX_KERNEL_LAPLACIAN_PYRAMID',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef('laplacian', kpOutput, kpRequired, s_vx_pyramid, 'VX_PYRAMID_FORMAT is VX_DF_IMAGE_S16'),
    ParameterDef(s_output , kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]')
    ], 'output is input')

KernelDef('org.khronos.openvx.laplacian_reconstruct', 'vxLaplacianReconstructNode', 'VX_KERNEL_LAPLACIAN_RECONSTRUCT',
    [
    ParameterDef('laplacian', kpInput, kpRequired, s_vx_pyramid, 'VX_PYRAMID_FORMAT is VX_DF_IMAGE_S16'),
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]')
    ], 'output is input')

KernelDef('org.khronos.openvx.non_linear_filter', 'vxNonLinearFilterNode', 'VX_KERNEL_NON_LINEAR_FILTER',
    [
    ParameterDef('function', kpInput, kpImmutable, 'vx_non_linear_filter_e', ''),
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('mask', kpInput, kpRequired, s_vx_matrix, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.match_template', 'vxMatchTemplateNode', 'VX_KERNEL_MATCH_TEMPLATE',
    [
    ParameterDef(s_src, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('templateImage', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('matchingMethod', kpInput, kpImmutable, 'vx_comp_metric_e', ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_S16')
    ], 
    'output.VX_IMAGE_WIDTH is src.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is src.VX_IMAGE_HEIGHT and '
    'src.VX_IMAGE_WIDTH is templateImage.VX_IMAGE_WIDTH and src.VX_IMAGE_HEIGHT is templateImage.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.lbp', 'vxLBPNode', 'VX_KERNEL_LBP',
    [
    ParameterDef('in', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('format', kpInput, kpImmutable, 'vx_lbp_format_e', ''),
    ParameterDef('kernel_size', kpInput, kpImmutable, 'vx_int8', ''),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
    ], 'output is input')

KernelDef('org.khronos.openvx.hough_lines_p', 'vxHoughLinesPNode', 'VX_KERNEL_HOUGH_LINES_P',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('params', kpInput, kpImmutable, 'vx_hough_lines_p_t', ''),
    ParameterDef('lines_array', kpOutput, kpRequired, s_vx_array, 'VX_ARRAY_ELEM_TYPE is VX_TYPE_LINE_2D'),
    ParameterDef('num_lines', kpOutput, kpOptional, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_SIZE')
    ], '')

KernelDef('org.khronos.openvx.tensor_multiply', 'vxTensorMultiplyNode', 'VX_KERNEL_TENSOR_MULTIPLY',
    [
    ParameterDef(s_input1, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_input2, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('scale', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('overflow_policy', kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef('rounding_policy', kpInput, kpImmutable, 'vx_round_policy_e', ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_tensor, '')
    ], 'output is input1') #TODO: complex test relating input2 to input1

KernelDef('org.khronos.openvx.tensor_add', 'vxTensorAddNode', 'VX_KERNEL_TENSOR_ADD',
    [
    ParameterDef(s_input1, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_input2, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_policy, kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_tensor, '')
    ], 'output is input1') #TODO: complex test relating input2 to input1

KernelDef('org.khronos.openvx.tensor_subtract', 'vxTensorSubtractNode', 'VX_KERNEL_TENSOR_SUBTRACT',
    [
    ParameterDef(s_input1, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_input2, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_policy, kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_tensor, '')
    ], 'output is input1') #TODO: complex test relating input2 to input1

KernelDef('org.khronos.openvx.tensor_table_lookup', 'vxTensorTableLookupNode', 'VX_KERNEL_TENSOR_TABLELOOKUP',
    [
    ParameterDef(s_input1, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('lut', kpInput, kpRequired, s_vx_lut, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_tensor, '')
    ], 'lut.VX_LUT_TYPE is output.VX_TENSOR_DATA_TYPE and output is input1')

KernelDef('org.khronos.openvx.tensor_transpose', 'vxTensorTransposeNode', 'VX_KERNEL_TENSOR_TRANSPOSE',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_tensor, ''),
    ParameterDef('dimension1', kpInput, kpImmutable, s_vx_size, ''),
    ParameterDef('dimension2', kpInput, kpImmutable, s_vx_size, '')
    ], '') #TODO: crazy complex test on dimensions and values

KernelDef('org.khronos.openvx.tensor_convert_depth', 'vxTensorConvertDepthNode', 'VX_KERNEL_TENSOR_CONVERT_DEPTH',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_policy, kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef('norm', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('offset', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_tensor, '')
    ], '') #TODO: test that tensor output dimensions are the same as input dimensions

KernelDef('org.khronos.openvx.matrix_multiply', 'vxTensorMatrixMultiplyNode', 'VX_KERNEL_TENSOR_MATRIX_MULTIPLY',
    [
    ParameterDef(s_input1, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef(s_input2, kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('input3', kpInput, kpOptional, s_vx_tensor, ''),
    ParameterDef('matrix_multiply_params', kpInput, kpImmutable, 'vx_tensor_matrix_multiply_params_t', ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_tensor, '')
    ], '') #TODO: complex test...

    
KernelDef('org.khronos.openvx.copy', 'vxCopyNode', 'VX_KERNEL_COPY', 
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_reference, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_reference, '')
    ], 'output is input')

KernelDef('org.khronos.openvx.non_max_suppression', 'vxNonMaxSuppressionNode', 'VX_KERNEL_NON_MAX_SUPPRESSION',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]'),
    ParameterDef('mask', kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('win_size', kpInput, kpImmutable, s_vx_int32, '$odd($value)'), #TODO: extend parser to cope with $odd function
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGE_S16]')
    ], 'output is input and input.VX_IMAGE_WIDTH is mask.VX_IMAGE_WIDTH and input.VX_IMAGE_HEIGHT is mask.VX_IMAGE_HEIGHT')

KernelDef('org.khronos.openvx.scalar_operation', 'vxScalarOperationNode', 'VX_KERNEL_SCALAR_OPERATION',
    [
    ParameterDef('scalar_operation', kpInput, kpImmutable, 'vx_scalar_operation_e', ''),
    ParameterDef('a', kpInput, kpRequired, s_vx_scalar, ''),
    ParameterDef('b', kpInput, kpRequired, s_vx_scalar, ''), 
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_scalar, '')
    ], '') #TODO: tedious tests due to the nature of the beast

KernelDef('org.khronos.openvx.hog_features', 'vxHOGFeaturesNode', 'VX_KERNEL_HOG_FEATURES',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('magnitudes', kpInput, kpRequired, s_vx_tensor, 'VX_TENSOR_DATA_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('bins', kpInput, kpRequired, s_vx_tensor, 'VX_TENSOR_DATA_TYPE is VX_TYPE_INT8'),
    ParameterDef('params', kpInput, kpImmutable, 'vx_hog_t', ''),
    # The size is not a kernel parameter. We know that all structures must have their size passed to the
    # node creation function.
    # ParameterDef('hog_param_size', kpInput, kpSize, s_vx_size, '$value is $sizeof(vx_hog_t)'), # TODO: extend parser to cope with sizeof()
    ParameterDef('features', kpOutput, kpRequired, s_vx_tensor, 'VX_TENSOR_DATA_TYPE is VX_TYPE_FLOAT32')
    ], '') #TODO: test dimensions of tensors

KernelDef('org.khronos.openvx.hog_cells', 'vxHOGCellsNode', 'VX_KERNEL_HOG_CELLS',
    [
    ParameterDef(s_input, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8'),
    ParameterDef('cell_width', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('cell_height', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('num_bins', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('magnitudes', kpOutput, kpRequired, s_vx_tensor, 'VX_TENSOR_DATA_TYPE is VX_TYPE_FLOAT32'),
    ParameterDef('bins', kpOutput, kpRequired, s_vx_tensor, 'VX_TENSOR_DATA_TYPE is VX_TYPE_INT8')
    ], '') #TODO: test dimensions of tensors

KernelDef('org.khronos.openvx.bilateral_filter', 'vxBilateralFilterNode', 'VX_KERNEL_BILATERAL_FILTER',
    [
    ParameterDef(s_src, kpInput, kpRequired, s_vx_tensor, 'VX_TENSOR_DATA_TYPE in [VX_TYPE_UINT8, VX_TYPE_INT16] and VX_TENSOR_NUMBER_OF_DIMS in [2,3]'),
    ParameterDef('diameter', kpInput, kpImmutable, s_vx_int32, '$odd($value) and 3 < $value < 10'),
    ParameterDef('sigmaSpace', kpInput, kpImmutable, 'vx_float32', '0 < $value <= 20'),
    ParameterDef('sigmaValues', kpInput, kpImmutable, 'vx_float32', '0 < $value <= 20'),
    ParameterDef(s_dst, kpOutput, kpRequired, s_vx_tensor, 'VX_TENSOR_DATA_TYPE in [VX_TYPE_UINT8, VX_TYPE_INT16] and VX_TENSOR_NUMBER_OF_DIMS in [2,3]')
    ], 'output is input')

KernelDef('org.khronos.openvx.select', 'vxSelectNode', 'VX_KERNEL_SELECT',
    [
    ParameterDef('condition', kpInput, kpRequired, s_vx_scalar, 'VX_SCALAR_TYPE is VX_TYPE_BOOL'),
    ParameterDef('true_value', kpInput, kpRequired, s_vx_reference, ''),
    ParameterDef('false_value', kpInput, kpRequired, s_vx_reference, ''),
    ParameterDef(s_output, kpOutput, kpRequired, s_vx_reference, '')
    ], 'output is true_value and output is false_value')

KernelDef('org.khronos.openvx.min', 'vxMinNode', 'VX_KERNEL_MAX',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGES16]'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGES16]'),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGES16]')
    ], 'out is in1 and in2 is in1')

KernelDef('org.khronos.openvx.max', 'vxMaxNode', 'VX_KERNEL_MIN',
    [
    ParameterDef(s_in1, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGES16]'),
    ParameterDef(s_in2, kpInput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGES16]'),
    ParameterDef(s_out, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT in [VX_DF_IMAGE_U8, VX_DF_IMAGES16]')
    ], 'out is in1 and in2 is in1')

    # NN extension kernels
KernelDef('org.khronos.nn_extension.convolution_layer', 'vxConvolutionLayer', 'VX_KERNEL_CONVOLUTION_LAYER',
    [
    ParameterDef('inputs', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('weights', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('biases', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('convolution_params', kpInput, kpImmutable, 'vx_nn_convolution_params_t', ''),
    # The size is not a kernel parameter. We know that all structures must have their size passed to the
    # node creation function.
    # ParameterDef('size_of_convolution_params', kpInput, kpSize, s_vx_size, ''),
    ParameterDef('outputs', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.nn_extension.fully_connected_layer', 'vxFullyConnectedLayer', 'VX_KERNEL_FULLY_CONNECTED_LAYER',
    [
    ParameterDef('inputs', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('weights', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('biases', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('overflow_policy', kpInput, kpImmutable, 'vx_convert_policy_e', ''),
    ParameterDef('rounding_policy', kpInput, kpImmutable, 'vx_round_policy_e', ''),
    ParameterDef('outputs', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.nn_extension.pooling_layer', 'vxPoolingLayer', 'VX_KERNEL_POOLING_LAYER',
    [
    ParameterDef('inputs', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('pooling_type', kpInput, kpImmutable, 'vx_nn_pooling_type_e', ''),
    ParameterDef('pooling_size_x', kpInput, kpImmutable, s_vx_size, ''),
    ParameterDef('pooling_size_y', kpInput, kpImmutable, s_vx_size, ''),
    ParameterDef('pooling_padding_x', kpInput, kpImmutable, s_vx_size, ''),
    ParameterDef('pooling_padding_y', kpInput, kpImmutable, s_vx_size, ''),
    ParameterDef('rounding', kpInput, kpImmutable, 'vx_nn_rounding_type_e', ''),
    ParameterDef('outputs', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.nn_extension.softmax_layer', 'vxSoftmaxLayer', 'VX_KERNEL_SOFTMAX_LAYER',
    [
    ParameterDef('inputs', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('outputs', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.nn_extension.normalization_layer', 'vxNormalizationLayer', 'VX_KERNEL_NORMALIZATION_LAYER',
    [
    ParameterDef('inputs', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('type', kpInput, kpImmutable, 'vx_nn_norm_type_e', ''),
    ParameterDef('normalization_size', kpImmutable, kpRequired, s_vx_size, ''),
    ParameterDef('alpha', kpInput, kpImmutable, s_vx_float32, ''),
    ParameterDef('beta', kpInput, kpImmutable, s_vx_float32, ''),
    ParameterDef('outputs', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.nn_extension.activation_layer', 'vxActivationLayer', 'VX_KERNEL_ACTIVATION_LAYER',
    [
    ParameterDef('inputs', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('function', kpInput, kpImmutable, 'vx_nn_activation_function_e', ''),
    ParameterDef('a', kpInput, kpImmutable, s_vx_float32, ''),
    ParameterDef('b', kpInput, kpImmutable, s_vx_float32, ''),
    ParameterDef('outputs', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.nn_extension.roi_pooling_layer', 'vxROIPoolingLayer', 'VX_KERNEL_ROI_POOLING_LAYER',
    [
    ParameterDef('input_data', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('input_rois', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('roi_pool_params', kpInput, kpImmutable, 'vx_nn_roi_pool_params_t', ''),
    # The size is not a kernel parameter. We know that all structures must have their size passed to the
    # node creation function.
    # ParameterDef('size_of_roi_params', kpInput, kpSize, s_vx_size, ''),
    ParameterDef('output_arr', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.nn_extension.deconvolution_layer', 'vxDeconvolutionLayer', 'VX_KERNEL_DECONVOLUTION_LAYER',
    [
    ParameterDef('inputs', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('weights', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('biases', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('deconvolution_params', kpInput, kpImmutable, 'vx_nn_deconvolution_params_t', ''),
    # The size is not a kernel parameter. We know that all structures must have their size passed to the
    # node creation function.
    # ParameterDef('size_of_deconv_params', kpInput, kpSize, s_vx_size, ''),
    ParameterDef('outputs', kpOutput, kpRequired, s_vx_tensor, '')
    ],'')
KernelDef('org.khronos.clasifier_extension.scan_classifier', 'vxScanClassifierNode', 'VX_KERNEL_SCAN_CLASSIFIER',
    [
    ParameterDef('input_feature_map', kpInput, kpRequired, s_vx_tensor, ''),
    ParameterDef('model', kpInput, kpImmutable, 'vx_classifier_model', ''),
    ParameterDef('scanwindow_width', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('scanwindow_height', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('step_x', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('step_y', kpInput, kpImmutable, s_vx_int32, ''),
    ParameterDef('object_confidences', kpOutput, kpOptional, s_vx_array, ''),
    ParameterDef('object_rectangles', kpOutput, kpRequired, s_vx_array, ''),
    ParameterDef('num_objects', kpOutput, kpOptional, s_vx_array, '')
    ],'')

# extraKernels = {    # Just a couple of test ones for now
#     'com.img.openvx.test1', 'vxTest1Node', 'VX_IMG_KERNEL_TEST1',
#     [
#     ParameterDef(s_input, kpInput, kpRequired, s_vx_image, ''),
#     ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, '')
#     ], 'output.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT'),

#     'com.img.openvx.test2', 'vxTest2Node', 'VX_IMG_KERNEL_TEST2',
#     [
#     ParameterDef(s_input, kpInput, kpRequired, s_vx_image, ''),
#     ParameterDef('channel', kpInput, kpImmutable, 'vx_channel_e', ''),
#     ParameterDef(s_output, kpOutput, kpRequired, s_vx_image, 'VX_IMAGE_FORMAT is VX_DF_IMAGE_U8')
#     ], 'output.VX_IMAGE_WIDTH is input.VX_IMAGE_WIDTH and output.VX_IMAGE_HEIGHT is input.VX_IMAGE_HEIGHT')
# }

# def unknownKernel():
#     '''
#     Provide a means of introducing an unknown kernel.
#     There are 12 parameters, all optional inputs, and all of type vx_reference.
#     '''
#     return ('', 'VX_KERNEL_INVALID',
#     [
#     ParameterDef('input0', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef(s_input1, kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef(s_input2, kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input3', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input4', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input5', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input6', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input7', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input8', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input9', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input10', kpInput, kpOptional, s_vx_reference, ''),
#     ParameterDef('input11', kpInput, kpOptional, s_vx_reference, '')
#     ], '')