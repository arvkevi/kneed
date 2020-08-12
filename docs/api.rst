.. _api:

API Reference
=============

There are two classes in `kneed`: `KneeLocator` identifies the knee/elbow point(s) and and `DataGenerator` creates synthetic `x` and `y` numpy arrays to explore `kneed`.

KneeLocator
-----------

.. autoclass:: kneed.knee_locator.KneeLocator
    :exclude-members: plot_knee, plot_knee_normalized

Plotting methods
^^^^^^^^^^^^^^^^

There are two methods for basic visualizations of the knee/elbow point(s).

.. automethod:: kneed.knee_locator.KneeLocator.plot_knee
.. automethod:: kneed.knee_locator.KneeLocator.plot_knee_normalized

DataGenerator
-------------

.. automodule:: kneed.data_generator
   :members: