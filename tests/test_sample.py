import math
import matplotlib.pyplot as plt
import numpy as np
import pytest
from kneed.data_generator import DataGenerator as dg
from kneed.knee_locator import KneeLocator


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_figure2(interp_method):
    """From the kneedle manuscript"""
    x, y = dg.figure2()
    kl = KneeLocator(x, y, S=1.0, curve='concave', interp_method=interp_method)
    assert math.isclose(kl.knee, 0.22, rel_tol=0.05)
    assert math.isclose(kl.elbow, 0.22, rel_tol=0.05)
    assert math.isclose(kl.norm_elbow, kl.knee, rel_tol=0.05)


def test_NoisyGaussian():
    """From the Kneedle manuscript"""
    x, y = dg.noisy_gaussian(mu=50, sigma=10, N=1000, seed=42)
    kl = KneeLocator(x, y, S=1.0, curve='concave', interp_method='polynomial', polynomial_features=11, online=True)
    assert math.isclose(kl.knee, 63.0, rel_tol=1e-02)


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_increasing(interp_method):
    """test a concave increasing function"""
    x, y = dg().concave_increasing()
    kn = KneeLocator(x, y, curve='concave', interp_method=interp_method)
    assert kn.knee == 2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_decreasing(interp_method):
    """test a concave decreasing function"""
    x, y = dg.concave_decreasing()
    kn = KneeLocator(
        x, y, curve='concave', direction='decreasing', interp_method=interp_method
    )
    assert kn.knee == 7


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_increasing(interp_method):
    """test a convex increasing function"""
    x, y = dg.convex_increasing()
    kl = KneeLocator(x, y, curve='convex', interp_method=interp_method)
    assert kl.knee == 7


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_decreasing(interp_method):
    """test a convex decreasing function"""
    x, y = dg.convex_decreasing()
    kl = KneeLocator(
        x, y, curve='convex', direction='decreasing', interp_method=interp_method
    )
    assert kl.knee == 2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_increasing_truncated(interp_method):
    """test a truncated concave increasing function"""
    x, y = dg.concave_increasing()
    kl = KneeLocator(
        x[:-3] / 10, y[:-3] / 10, curve='concave', interp_method=interp_method
    )
    assert kl.knee == 0.2


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_concave_decreasing_truncated(interp_method):
    """test a truncated concave decreasing function"""
    x, y = dg.concave_decreasing()
    kl = KneeLocator(
        x[:-3] / 10,
        y[:-3] / 10,
        curve='concave',
        direction='decreasing',
        interp_method=interp_method,
    )
    assert kl.knee == 0.4


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_increasing_truncated(interp_method):
    """test a truncated convex increasing function"""
    x, y = dg.convex_increasing()
    kl = KneeLocator(
        x[:-3] / 10, y[:-3] / 10, curve='convex', interp_method=interp_method
    )
    assert kl.knee == 0.4


@pytest.mark.parametrize("interp_method", ['interp1d', 'polynomial'])
def test_convex_decreasing_truncated(interp_method):
    """test a truncated convex decreasing function"""
    x, y = dg.convex_decreasing()
    kl = KneeLocator(
        x[:-3] / 10,
        y[:-3] / 10,
        curve='convex',
        direction='decreasing',
        interp_method=interp_method,
    )
    assert kl.knee == 0.2


@pytest.mark.parametrize(
    "interp_method, expected", [('interp1d', 26), ('polynomial', 28)]
)
def test_convex_decreasing_bumpy(interp_method, expected):
    """test a bumpy convex decreasing function"""
    x, y = dg.bumpy()
    kl = KneeLocator(
        x, y, curve='convex', direction='decreasing', interp_method=interp_method
    )
    assert kl.knee == expected


@pytest.mark.parametrize("online, expected", [(True, 482), (False, 22)])
def test_gamma_online_offline(online, expected):
    """Tests online and offline knee detection.
    Notable that a large number of samples are highly sensitive to S parameter
    """
    np.random.seed(23)
    n = 1000
    x = range(1, n + 1)
    y = sorted(np.random.gamma(0.5, 1.0, n), reverse=True)
    kl = KneeLocator(x, y, curve='convex', direction='decreasing', online=online)
    assert kl.knee == expected


def test_sensitivity():
    """Test the S parameter -- where S is the number of flat points to identify before calling a knee"""
    np.random.seed(23)
    sensitivity = [1, 3, 5, 10, 100, 200, 400]
    detected_knees = []
    expected_knees = [43, 137, 178, 258, 305, 482, 482]
    n = 1000
    x = range(1, n + 1)
    y = sorted(np.random.gamma(0.5, 1.0, n), reverse=True)
    for s, expected_knee in zip(sensitivity, expected_knees):
        kl = KneeLocator(x, y, curve='convex', direction='decreasing', S=s)
        detected_knees.append(kl.knee)
        assert kl.knee, expected_knee


def test_sine():
    x = np.arange(0, 10, 0.1)
    y_sin = np.sin(x)

    sine_combos = [
        ('decreasing', 'convex'),
        ('increasing', 'convex'),
        ('increasing', 'concave'),
        ('decreasing', 'concave'),
    ]
    expected_knees = [4.5, 4.9, 7.7, 1.8]
    detected_knees = []
    for direction, curve in sine_combos:
        kl_sine = KneeLocator(
            x, y_sin, direction=direction, curve=curve, S=1, online=True
        )
        detected_knees.append(kl_sine.knee)
    assert np.isclose(expected_knees, detected_knees).all()


def test_list_input():
    """Indirectly test that flip works on lists as input"""
    x, y = dg.figure2()
    kl = KneeLocator(
        x.tolist(), y.tolist(), S=1.0, curve='concave', interp_method='polynomial'
    )
    assert math.isclose(kl.knee, 0.22, rel_tol=0.05)


def test_flat_maxima():
    """The global maxima has a sequentially equal value in the difference curve"""
    x = [
        0,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0,
        12.0,
        13.0,
        14.0,
        15.0,
        16.0,
        17.0,
    ]
    y = [
        1,
        0.787701317715959,
        0.7437774524158126,
        0.6559297218155198,
        0.5065885797950219,
        0.36749633967789164,
        0.2547584187408492,
        0.16251830161054173,
        0.10395314787701318,
        0.06734992679355783,
        0.043923865300146414,
        0.027818448023426062,
        0.01903367496339678,
        0.013177159590043924,
        0.010248901903367497,
        0.007320644216691069,
        0.005856515373352855,
        0.004392386530014641,
    ]
    # When S=0.0 the first local maximum is found.
    kl = KneeLocator(x, y, curve='convex', direction='decreasing', S=0.0)
    assert math.isclose(kl.knee, 1.0, rel_tol=0.05)

    # When S=1.0 the global maximum is found.
    kl = KneeLocator(x, y, curve='convex', direction='decreasing', S=1.0)
    assert math.isclose(kl.knee, 8.0, rel_tol=0.05)


def test_all_knees():
    x, y = dg.bumpy()
    kl = KneeLocator(x, y, curve='convex', direction='decreasing', online=True)
    assert np.isclose(sorted(kl.all_elbows), [26, 31, 41, 46, 53]).all()
    assert np.isclose(sorted(kl.all_norm_elbows), [
            0.2921348314606742,
            0.348314606741573,
            0.4606741573033708,
            0.5168539325842696,
            0.5955056179775281,
    ]
                      ).all()


def test_y():
    """Test the y value"""
    x, y = dg.figure2()
    kl = KneeLocator(x, y, S=1.0, curve="concave", interp_method="interp1d")
    assert math.isclose(kl.knee_y, 1.897, rel_tol=0.03)
    assert math.isclose(kl.all_knees_y[0], 1.897, rel_tol=0.03)
    assert math.isclose(kl.norm_knee_y, 0.758, rel_tol=0.03)
    assert math.isclose(kl.all_norm_knees_y[0], 0.758, rel_tol=0.03)

    assert math.isclose(kl.elbow_y, 1.897, rel_tol=0.03)
    assert math.isclose(kl.all_elbows_y[0], 1.897, rel_tol=0.03)
    assert math.isclose(kl.norm_elbow_y, 0.758, rel_tol=0.03)
    assert math.isclose(kl.all_norm_elbows_y[0], 0.758, rel_tol=0.03)


def test_y_no_knee():
    """Test the y value, if there is no knee found."""
    kl = KneeLocator(
        np.array([1, 2, 3]),
        np.array([0.90483742, 0.81873075, 0.74081822]),
        S=1.0,
        curve="convex",
        direction="decreasing",
        interp_method="interp1d",
        online=False,
    )
    assert kl.knee_y is None
    assert kl.norm_knee_y is None


def test_interp_method():
    """Test that the interp_method argument is valid."""
    x, y = dg.figure2()
    with pytest.raises(ValueError):
        kl = KneeLocator(x, y, interp_method='not_a_method')


def test_x_equals_y():
    """Test that a runtime warning is raised when no maxima are found"""
    x = range(10)
    y = [1] * len(x)
    with pytest.warns(RuntimeWarning):
        kl = KneeLocator(x, y)


def test_plot_knee_normalized():
    """Test that plotting is functional"""
    x, y = dg.figure2()
    kl = KneeLocator(x, y, S=1.0, curve="concave", interp_method="interp1d")
    num_figures_before = plt.gcf().number
    kl.plot_knee_normalized()
    num_figures_after = plt.gcf().number
    assert num_figures_before < num_figures_after


def test_plot_knee():
    """Test that plotting is functional"""
    x, y = dg.figure2()
    kl = KneeLocator(x, y, S=1.0, curve="concave", interp_method="interp1d")
    num_figures_before = plt.gcf().number
    kl.plot_knee()
    num_figures_after = plt.gcf().number
    assert num_figures_before < num_figures_after


def test_logistic():
    y = np.array([2.00855493e-45, 1.10299045e-43, 4.48168384e-42, 1.22376580e-41,
                  5.10688883e-40, 1.18778110e-38, 5.88777891e-35, 4.25317895e-34,
                  4.06507035e-33, 6.88084518e-32, 2.99321831e-31, 1.13291723e-30,
                  1.05244482e-28, 2.67578448e-27, 1.22522190e-26, 2.36517846e-26,
                  8.30369408e-26, 1.24303033e-25, 2.27726918e-25, 1.06330422e-24,
                  5.55017673e-24, 1.92068553e-23, 3.31361011e-23, 1.13575247e-22,
                  1.75386416e-22, 6.52680518e-22, 2.05106011e-21, 6.37285545e-21,
                  4.16125535e-20, 1.12709507e-19, 5.75853420e-19, 1.73333796e-18,
                  2.70099890e-18, 7.53254646e-18, 1.38139433e-17, 3.60081965e-17,
                  8.08419977e-17, 1.86378584e-16, 5.36224556e-16, 8.89404640e-16,
                  2.34045104e-15, 4.72168880e-15, 6.84378992e-15, 2.26898430e-14,
                  3.10087652e-14, 2.78081199e-13, 1.06479577e-12, 2.81002203e-12,
                  4.22067092e-12, 9.27095863e-12, 1.54519738e-11, 4.53347819e-11,
                  1.35564441e-10, 2.35242087e-10, 4.45253545e-10, 9.78613696e-10,
                  1.53140922e-09, 2.81648560e-09, 6.70890436e-09, 1.49724785e-08,
                  5.59553565e-08, 1.39510811e-07, 7.64761811e-07, 1.40723957e-06,
                  4.97638863e-06, 2.12817943e-05, 3.26471410e-05, 1.02599591e-04,
                  3.18774179e-04, 5.67297630e-04, 9.22732716e-04, 1.17445643e-03,
                  3.59279384e-03, 3.61936491e-02, 6.39493416e-02, 1.29304829e-01,
                  1.72272215e-01, 3.46945901e-01, 5.02826602e-01, 6.24800042e-01,
                  7.38412957e-01, 7.59931663e-01, 7.73374421e-01, 7.91421897e-01,
                  8.29325597e-01, 8.57718637e-01, 8.73286061e-01, 8.77056835e-01,
                  8.93173768e-01, 9.05435646e-01, 9.17217910e-01, 9.19119179e-01,
                  9.24810910e-01, 9.26306908e-01, 9.28621233e-01, 9.33855835e-01,
                  9.37263027e-01, 9.41651642e-01])
    x = np.array([1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13.,
                  14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25., 26.,
                  27., 28., 29., 30., 31., 32., 33., 34., 35., 36., 37., 38., 39.,
                  40., 41., 42., 43., 44., 45., 46., 47., 48., 49., 50., 51., 52.,
                  53., 54., 55., 56., 57., 58., 59., 60., 61., 62., 63., 64., 65.,
                  66., 67., 68., 69., 70., 71., 72., 73., 74., 75., 76., 77., 78.,
                  79., 80., 81., 82., 83., 84., 85., 86., 87., 88., 89., 90., 91.,
                  92., 93., 94., 95., 96., 97., 98.])
    kl = KneeLocator(
        x,
        y,
        curve="convex",
        direction="increasing",
        online=True,
    )
    assert kl.knee == 73

