from kotti.resources import Document


def test_get_source(translated_docs, db_session):
    from kotti_multilingual.api import get_source

    source, target = translated_docs
    assert get_source(target) is source


def test_get_source_none(root, db_session):
    from kotti_multilingual.api import get_source

    assert get_source(root) is None


def test_get_translations(translated_docs, db_session):
    from kotti_multilingual.api import get_translations

    source, target = translated_docs
    assert get_translations(source) == {'sl': target}


def test_get_translations_none(root, db_session):
    from kotti_multilingual.api import get_translations

    assert get_translations(root) == {}


def test_link_translation(multilingual_doc, db_session):
    from kotti_multilingual.api import link_translation
    from kotti_multilingual.api import get_translations

    doc2 = multilingual_doc['doc2'] = Document(language=u'sl')
    link_translation(multilingual_doc, doc2)

    assert get_translations(multilingual_doc) == {'sl': doc2}


def test_unlink_translation(translated_docs, db_session):
    from kotti_multilingual.api import unlink_translation
    from kotti_multilingual.api import get_translations

    source, target = translated_docs
    unlink_translation(target)

    assert get_translations(source) == {}


def test_get_languages_no_language_root(root):
    from kotti_multilingual.api import get_languages

    assert get_languages() == []


def test_get_languages_no_request(root):
    from kotti_multilingual.api import get_languages
    from kotti_multilingual.resources import LanguageRoot

    root['de'] = LanguageRoot(language=u'de')

    assert get_languages() == [{'id': u'de', 'title': u'Deutsch'}]


def test_get_languages_request(root, dummy_request):
    from kotti_multilingual.api import get_languages
    from kotti_multilingual.resources import LanguageRoot

    root['de'] = LanguageRoot(language=u'de')

    assert get_languages(dummy_request) == [
        {'id': u'de', 'title': u'Deutsch', 'url': u'http://example.com/de/'}]


def test_get_languages_no_permissions(config, root, dummy_request):
    from kotti_multilingual.api import get_languages
    from kotti_multilingual.resources import LanguageRoot

    root['de'] = LanguageRoot(language=u'de')
    assert get_languages(dummy_request) == [
        {'id': u'de', 'title': u'Deutsch', 'url': u'http://example.com/de/'}]
    config.testing_securitypolicy(permissive=False)
    assert get_languages(dummy_request) == []