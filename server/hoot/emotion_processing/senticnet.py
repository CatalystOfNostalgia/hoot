import sys
import rdflib
import requests

from rdflib import URIRef

BASE_URI = 'http://sentic.net/api'


class Senticnet(object):
    """
    Simple API to use Senticnet 3 without be bothered by RDF stuff.
    """
    def __init__(self):
        self.concept_base_uri = BASE_URI + '/en/concept/'

    def concept_local(self, concept, g):
        """
        Return all the information abou a concept from the local sentic db.
        g must be a parsed RDF graph containing the sentic values.
        """
        if (None, None, concept) not in g:
            # debug statement
            #print("{} not found in database!".format(concept))
            return {}

        result = {'sentics': {}}

        # find the subject, the return generator will always have 1 object
        subject = next(g.subjects(URIRef(BASE_URI + 'text'), concept))

        for s, p, o in g.triples((subject, None, None)):
            value = o.toPython()
            if p == URIRef(BASE_URI + 'pleasantness'):
                result['sentics']['pleasantness'] = value
            elif p == URIRef(BASE_URI + 'aptitude'):
                result['sentics']['aptitude'] = value
            elif p == URIRef(BASE_URI + 'sensitivity'):
                result['sentics']['sensitivity'] = value
            elif p == URIRef(BASE_URI + 'attention'):
                result['sentics']['attention'] = value
            elif p == URIRef(BASE_URI + 'polarity'):
                result['polarity'] = value

        return result

    def concept_api(self, concept):
        """
        Return all the information about a concept: semantics,
        sentics and polarity.
        """
        parsed_graph = None
        result = {}

        try:
            result["polarity"] = self.polarity(concept, parsed_graph)
            result["sentics"] = self.sentics(concept, parsed_graph)
            result["semantics"] = self.semantics(concept, parsed_graph)
        except:
            print("{} not found in database!".format(concept))
            return {}

        sys.stdout.write('got values for: {}                \r'.format(concept))
        sys.stdout.flush()
        return result

    def semantics_api(self, concept, parsed_graph=None):
        """
        Return the semantics associated with a concept.
        If you pass a parsed graph, the method do not load the rdf again.
        """
        concept_semantics_uri = self.concept_base_uri + concept + "/semantics"
        _, result = self._output(concept_semantics_uri)

        return [str(self._last_uri_element(x)) for x in result]

    def sentics_api(self, concept, parsed_graph=None):
        """
        Return sentics of a concept.
        If you pass a parsed graph, the method do not load the rdf again.
        """
        concept_sentics_uri = self.concept_base_uri + concept + "/sentics"
        sentics = {
            "pleasantness": 0,
            "attention": 0,
            "sensitivity": 0,
            "aptitude": 0
        }

        if parsed_graph is None:
            graph = rdflib.Graph()
            parsed_graph = graph.parse(concept_sentics_uri, format="xml")

        result, _ = self._output(concept_sentics_uri)

        sentics["pleasantness"] = result[3]
        sentics["attention"] = result[0]
        sentics["sensitivity"] = result[1]
        sentics["aptitude"] = result[2]

        return sentics

    def polarity(self, concept, parsed_graph=None):
        """
        Return the polarity of a concept.
        If you pass a parsed graph, the method do not load the rdf again.
        """
        concept_polarity_uri = self.concept_base_uri+concept+"/polarity"

        if parsed_graph is None:
            try:
                graph = rdflib.Graph()
                parsed_graph = graph.parse(concept_polarity_uri, format="xml")
                result, _ = self._output(concept_polarity_uri)
                return result[0]

            except Exception:
                return 0

    def _last_uri_element(self, uri):
        return uri.split("/")[-1]

    def _output(self, url):
        """
        Downloads and returns the output avoiding w3.org error
        """
        response = requests.get(url)
        html = response.text
        html = html.replace('w3.org', 'www.w3.org')

        graph = rdflib.Graph()
        parsed_graph = graph.parse(data=html, format="xml")

        result = []
        stresult = []

        for s, p, o in parsed_graph:
            if type(o) == rdflib.term.Literal:
                result.append(o.toPython())
            else:
                stresult.append(o.toPython())

        return result, stresult
