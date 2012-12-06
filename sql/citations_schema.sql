/**
 *
Schema Description
------------------------

Patent:   8 character alphanumeric identification assigned by the USTPO
Citation: Patent that is cited by the defined patent.
Cit_Date: Patent grant date cited by defined Patent
Cit_Name: Patent primary inventor surname cited by defined patent
Cit_Kind: Patent kind codes (defined in Appendix 2) cited by defined patent
Cit_Name: Lastname of primary inventor of the cited patent
Category: Cited source of patent (Cited by examiner, other)
Cit_Name: LastnameSeqNumber Citation sequence (0 = first citation)
*/

/**
 * Citations in the SQLite3 files are
 * split. This table covers years 2000
 * through 2010. Schemas for other years
 * are identical.
 */
CREATE TABLE citation00_10 (
  Patent      VARCHAR(8),
  Cit_Date    INTEGER,
  Cit_Name    VARCHAR(10),
  Cit_Kind    VARCHAR(1),
  Cit_Country VARCHAR(2),
  Citation    VARCHAR(8),
  Category    VARCHAR(15),
  CitSeq      INTEGER);


CREATE UNIQUE INDEX idx_idx1 ON citation00_10 (patent,citation);
CREATE INDEX idx_idx2 ON citation00_10 (citation);
CREATE INDEX idx_idx3 ON citation00_10 (patent);

-- More information
/**
 *
The development of patents is oftentimes based on research from previous
patents, known simply as a citation.  Within the USPTO XML file,
citations are organized numerically through a patent citation number reference.
The document number mimics the format that constitutes the previously
mentioned patent number and type.  Here we are able to determine that
this patent’s first citation is to design patent #20662 and its 38th
citation is to design patent #540507.

<references-cited>
  <citation>
    <patcit num="00001">
      <document-id>
                ……
        <doc-number>D20662</doc-number>
                ……
      </document-id>
    </patcit>
        ……
  </citation>
    ……
  <citation>
    <patcit num="00038">
      <document-id>
                ……
        <doc-number>D540507</doc-number>
                ……
      </document-id>
    </patcit>
        ……
  </citation>
</references-cited>


*/

