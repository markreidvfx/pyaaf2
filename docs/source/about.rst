About the AAF File Format
=========================

AAF is a file format used for professional multimedia creation and authoring.
The file specification is managed by the `Advanced Media Workflow Association
(AMWA) <https://www.amwa.tv/>`_.

AAF uses a object-oriented data model. The data model has a single inheritance
class hierarchy and classes have properties that store metadata.  Classes, properties,
and types each have unique ids, known as a Authoring Unique Identifier (AUID).
AAF and MXF are closely related, The AAF data model is the basis for the MXF data model.

The Compound File Binary Format (CFBF) is what AAF uses for binary storage.  CFBF,
also called Structured Storage or Object Linking and Embedding (OLE), is a file format developed
by Microsoft for storing hierarchical data.  CFBF is basically a FAT32 filesystem
in a file and AAF uses "directories" as classes and "files" to store property metadata.

Further Reading
---------------

- `aafobjectspec-v1.1.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafobjectspec-v1.1.pdf?format=raw>`_
- `aafeditprotocol.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafeditprotocol.pdf?format=raw>`_
- `aafstoredformatspec-v1.0.1.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafstoredformatspec-v1.0.1.pdf?format=raw>`_
- `aafcontainerspec-v1.0.1.pdf <https://sourceforge.net/p/aaf/code2/ci/master/tree/doc/aafcontainerspec-v1.0.1.pdf?format=raw>`_
- `AAF SDK <http://aaf.sourceforge.net>`_
- `Media Authoring with Java API (MAJ) <https://github.com/AMWA-TV/maj>`_
- `Advanced Authoring Format Wikipedia <https://en.wikipedia.org/wiki/Advanced_Authoring_Format>`_
- `Compound File Binary Format Wikipedia <https://en.wikipedia.org/wiki/Compound_File_Binary_Format>`_
- `COM Structured Storage Wikipedia <https://en.wikipedia.org/wiki/COM_Structured_Storage>`_
