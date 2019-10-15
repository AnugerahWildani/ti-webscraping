import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
test_data = os.path.join(BASE_DIR, 'test-data')

# urls = [
#     'https://app.forskningsradet.no/mittNettstedWeb//portlets/prosjekt/prosjekter.do'
# ]

urls = [
    os.path.join(test_data, 'Adax', 'adax_mittNettstedWeb_portlets_prosjekt_prosjekter.do_.html'),
    os.path.join(test_data, 'Adax', 'adax_mittNettstedWeb_portlets_prosjekt_visDetaljerSkattefunn.doprojectId=305708_.html'),
    os.path.join(test_data, 'Memory', 'memory_mittNettstedWeb_portlets_prosjekt_visDetaljerSkattefunn.doprojectId=304184_.html'),
    os.path.join(test_data, 'generic', 'generic_mittNettstedWeb_portlets_prosjekt_prosjekter.do_.html'),
    os.path.join(test_data, 'Cavai', 'cavai_mittNettstedWeb_portlets_prosjekt_soknader.do_.html'), 
    os.path.join(test_data, 'Bioner', 'bioner_mittNettstedWeb_portlets_prosjekt_soknader.do_.html'), 
    os.path.join(test_data, 'generic', 'generic_mittNettstedWeb_portlets_prosjekt_soknader.do_.html'),
    os.path.join(test_data, 'generic', 'generic_mittNettstedWeb_portlets_soknad_begin.do_.html'),
    os.path.join(test_data, 'Cavai', 'cavai_mittNettstedWeb_portlets_soknad_begin.do_.html'), 
    os.path.join(test_data, 'Bioner', 'bioner_mittNettstedWeb_portlets_soknad_begin.do_.html'),
    os.path.join(test_data, 'Adax', 'adax_mittNettstedWeb_portlets_soknad_begin.do_.html'), 
    os.path.join(test_data, 'Memory', 'memory_mittNettstedWeb_portlets_soknad_begin.do_.html'),
    os.path.join(test_data, 'Memory', 'memory_mittNettstedWeb_portlets_prosjekt_visDetaljerSkattefunn.doprojectId=269913_.html')
]

urls_main = [
    os.path.join(test_data, 'Adax', 'adax_nomittNettstedWeb_.html'),
    os.path.join(test_data, 'Bioner', 'bioner_nomittNettstedWeb_.html'),
    os.path.join(test_data, 'Cavai', 'cavai_nomittNettstedWeb_.html'),
    os.path.join(test_data, 'Memory', 'memory_nomittNettstedWeb_.html')
]