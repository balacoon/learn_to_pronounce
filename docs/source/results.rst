Results
=======

Performance of FST-based pronunciation models on various corpora.

en_us
-----

Most commonly used pronunciation dictionary for en_us is cmudict.

+----------------------------------+-------------+------------+------------------+--------------+--------------------+
| data-set                         | ngram-order | model-size | train/test words | WER/PER      | WER/PER w/o stress |
+==================================+=============+============+==================+==============+====================+
| `CMUDict PRONASYL 2007`_         |      8      |   35 mB    | 106837 / 12000   | -            | 24.46 / 2.92       |
+----------------------------------+-------------+------------+------------------+--------------+--------------------+
| `CMUDict ARPA`_                  |      8      |   42 mB    | 113628/11978     | 32.48 / 4.18 | 24.8 / 2.95       |
+----------------------------------+-------------+------------+------------------+--------------+--------------------+
| `CMUDict X-SAMPA`_ from Balacoon |      8      |   42 mB    | 113628/11978     | 32.26 / 4.39 | 25.2 / 3.27        |
+----------------------------------+-------------+------------+------------------+--------------+--------------------+

.. _CMUDict PRONASYL 2007: https://sourceforge.net/projects/cmusphinx/files/G2P%20Models/phonetisaurus-cmudict-split.tar.gz
.. _CMUDict ARPA: https://github.com/cmusphinx/cmudict
.. _CMUDict X-SAMPA: https://github.com/balacoon/en_us_pronunciation/tree/main/cmudict