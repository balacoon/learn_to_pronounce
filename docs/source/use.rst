Usage
=====

In order to build pronunciation addon:

1. get the repo

.. code-block::

   git clone git@github.com:balacoon/learn_to_pronounce.git

2. build docker that manages all the dependencies

.. code-block::

    # if "build-fe" is specified, balacoon_frontend
    # is built from sources. You need special access for it
    # which you likely dont have.
    bash docker/build.sh [--build-fe]

3. get pronunciation resources. Adjust those if needed, but don't
   forget to share changes as a contribution. In order to promote
   multi-linguality, a unified phoneme set is used by the balacoon.
   You can find more information on decisions made in the `post`_.
   If you want to build a pronunciation generation for a new lexicon,
   you would need to perform mapping into Balacoon unified phoneme set.
   Check info on `mapping`_ of CMUDict as an example.

.. code-block::

    # resources are stored as submodules, pick one you need
    # from resources dir
    git submodule update --init resources/en_us_pronunciation/

4. launch docker and execute addon creation (includes lexicon packing,
   FST-based pronunciation generation training). To takes some time to
   run the training. At the end evaluation on withheld words is executed
   (if test_words are specified in resourced directory). Accuracy of
   pronunciation generation heavily depends on the language.

.. code-block::

   # script is really simple shortcut to start container. Adjust it
   # if needed
   bash docker/run.sh
   # check that everything works on a toy lexicon.
   learn_to_pronounce --locale en_us --work-dir toy_work_dir \
       --resources resources/en_us_pronunciation/toy/
   # if everything finishes without errors, time build complete addon.
   # check arguments of learn_to_pronounce to learn more on usage.
   learn_to_pronounce --locale en_us --out en_us_pronunciation.addon \
       --resources resources/en_us_pronunciation/cmudict 

5. learn_to_pronounce contains interactive demos that showcase how to use
   obtained artifacts.

.. code-block::

   # generating pronunciation with trained fst:
   demo_fst --fst work_dir/pronunciation.fst
   # using whole addon: looks up word in lexicon, if not found
   # generates pronunciation with FST-based model.
   # additionally, can spell words letter-by-letter
   demo_pronounce --addon en_us_pronunciation.addon [--spelling]

.. _post: https://balacoon.com/blog/balacoon_phonemeset/
.. _mapping: https://github.com/balacoon/en_us_pronunciation/blob/f683b7c4d9ad8baad048b3ff8bb9f8e900ccab43/cmudict/README.md