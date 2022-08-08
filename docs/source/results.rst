Results
=======

Performance of FST-based pronunciation models on various corpora.

en_us
-----

Most commonly used pronunciation dictionary for en_us is cmudict.

+----------------------------------+-------------+------------+------------------+--------------+--------------------+
| data-set                         | ngram-order | model-size | train/test words | WER/PER      | WER/PER w/o stress |
+==================================+=============+============+==================+==============+====================+
| `CMUDict PRONASYL 2007`_         |      8      |   32 mB    | 106837 / 12000   | -            | 28.89 / 4.48       |
+----------------------------------+-------------+------------+------------------+--------------+--------------------+
| `CMUDict ARPA`_                  |      8      |   34 mB    | 113628/11978     | 40.52 / 7.38 | 33.54 / 6.11       |
+----------------------------------+-------------+------------+------------------+--------------+--------------------+
| `CMUDict X-SAMPA`_ from Balacoon |      8      |   33 mB    | 113628/11978     | 44.19 / 8.87 | 37.8 / 7.72        |
+----------------------------------+-------------+------------+------------------+--------------+--------------------+

.. _CMUDict PRONASYL 2007: https://sourceforge.net/projects/cmusphinx/files/G2P%20Models/phonetisaurus-cmudict-split.tar.gz
.. _CMUDict ARPA: https://github.com/cmusphinx/cmudict
.. _CMUDict X-SAMPA: https://github.com/balacoon/en_us_pronunciation/tree/main/cmudict