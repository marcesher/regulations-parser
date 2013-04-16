#vim: set encoding=utf-8
import string
from pyparsing import OneOrMore, Optional, Regex, Suppress, Word
from pyparsing import getTokensEndLoc, ParseResults

def keep_pos(source, location, tokens):
    """Wrap the tokens with a class that also keeps track of the match's
    location."""
    return (WrappedResult(tokens, location, getTokensEndLoc()),)

class WrappedResult():
    """Keep track of matches along with their position. This is a bit of a
    hack to get around PyParsing's tendency to drop that info."""
    def __init__(self, tokens, start, end):
        self.tokens = tokens
        self.pos = (start, end)
    def __getattr__(self, attr):
        return getattr(self.tokens, attr)

lower_p = (
        Suppress("(") 
        + Word(string.ascii_lowercase).setResultsName("level1") 
        + Suppress(")"))
digit_p = (
        Suppress("(") 
        + Word(string.digits).setResultsName("level2") 
        + Suppress(")"))
roman_p = (
        Suppress("(") 
        + Word("ivxlcdm").setResultsName("level3") + 
        Suppress(")"))
upper_p = (
        Suppress("(") 
        + Word(string.ascii_uppercase).setResultsName("level4") 
        + Suppress(")"))

depth3_p = roman_p + Optional(upper_p)
depth2_p = digit_p + Optional(depth3_p)
depth1_p = lower_p + Optional(depth2_p)

any_depth_p = (
        depth1_p.setResultsName("depth1_p") 
        | depth2_p.setResultsName("depth2_p") 
        | depth3_p.setResultsName("depth3_p") 
        | upper_p.setResultsName("depth4_p"))

and_phrases = Suppress(Regex(",|and|or") + Optional("and"))

paragraph_tail = OneOrMore(and_phrases +
        any_depth_p.setParseAction(keep_pos).setResultsName("p_tail",
            listAllMatches=True)
        )

single_section = (
        Word(string.digits).setResultsName("part")
        + Suppress(".")
        + Word(string.digits).setResultsName("section")
        + Optional(depth1_p.setParseAction(keep_pos).setResultsName("p_head")
            + Optional(paragraph_tail))
        ).setParseAction(keep_pos)

single_section_with_marker = (
        Suppress(u"§") 
        + single_section.setResultsName("without_marker"))

multiple_sections = (
        Suppress(u"§§")
        + single_section.setResultsName("s_head")
        + OneOrMore(and_phrases 
            + single_section.setResultsName("s_tail", listAllMatches=True)))

single_paragraph = (
        Suppress("paragraph") 
        + any_depth_p.setResultsName("p_head")
        )

multiple_paragraphs = (
        Suppress("paragraphs") 
        + any_depth_p.setResultsName("p_head")
        + paragraph_tail)

any_citation = (
    multiple_sections.setResultsName("multiple_sections") 
    | single_section_with_marker.setResultsName("single_section")
    | single_paragraph.setResultsName("single_paragraph") 
    | multiple_paragraphs.setResultsName("multiple_paragraphs"))