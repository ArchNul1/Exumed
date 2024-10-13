import aiohttp
import asyncio
import time
import random
import re


class Dorks:
    def __init__(self, input = "") -> None:
        
        self.input = input
        self.urls = [
            
        #cpf e dados confidenciais
        f'https://www.google.com/search?q=inurl:"{self.input}" intext:"cpf" filetype:pdf OR filetype:txt OR filetype:doc',
        f'https://www.google.com/search?q="intext:"confidential" filetype:pdf OR filetype:txt OR filetype:doc',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"password" filetype:pdf OR filetype:txt OR filetype:doc',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"credentials" filetype:pdf OR filetype:txt OR filetype:doc',

        # Arquivos DOC/DOCX
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"confidential" filetype:doc OR filetype:docx',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"password" filetype:doc OR filetype:docx',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"internal use only" filetype:doc OR filetype:docx',

        # Arquivos TXT contendo senhas
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"passwords" filetype:txt',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"credentials" filetype:txt',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"ftp" filetype:txt',

        # Arquivos de Configuração
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"DB_PASSWORD" filetype:env OR filetype:conf OR filetype:ini',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"password" filetype:xml OR filetype:conf OR filetype:ini',

        # Logs
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"error" filetype:log',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"password" filetype:log',

        # Backups e Dumps
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"dump" filetype:sql OR filetype:bak',

        # Currículos
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"curriculum" filetype:pdf OR filetype:doc OR filetype:docx',

        # Relatórios
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"relatório" filetype:pdf OR filetype:doc OR filetype:xls OR filetype:xlsx',

        # Comprovantes de Pagamento
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"comprovante de pagamento" filetype:pdf OR filetype:jpg OR filetype:png',

        # Contratos
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"contrato" filetype:pdf OR filetype:doc OR filetype:docx',

        # Notas Fiscais
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"nota fiscal" filetype:pdf OR filetype:jpg OR filetype:png',

        # Documentos de Recursos Humanos
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"folha de pagamento" filetype:pdf OR filetype:doc',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"aviso de férias" filetype:pdf OR filetype:doc',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"contrato de trabalho" filetype:pdf OR filetype:doc',

        # Dados financeiros e contábeis
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"balanço patrimonial" filetype:xls OR filetype:pdf',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"demonstrativo de resultados" filetype:xls OR filetype:pdf',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"comprovante de pagamento" filetype:pdf OR filetype:jpg',

        # Documentos de Auditoria
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"relatório de auditoria" filetype:pdf OR filetype:doc',
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"auditoria interna" filetype:pdf OR filetype:doc',

        # Informações de Login
        f'https://www.google.com/search?q=intext:"login" inurl:"{self.input}" filetype:xls OR filetype:csv',
        f'https://www.google.com/search?q=intext:"username" inurl:"{self.input}" filetype:xls OR filetype:csv',

        # Exposed Directories
        f'https://www.google.com/search?q=intitle:"index of" inurl:"{self.input}" intext:"backup"',
        f'https://www.google.com/search?q=intitle:"index of" inurl:"{self.input}" intext:"config"',
        f'https://www.google.com/search?q=intitle:"index of" inurl:"{self.input}" intext:"admin"',

        # Open Ports
        f'https://www.google.com/search?q=intitle:"index of" inurl:"{self.input}/ssh"',
        f'https://www.google.com/search?q=intitle:"index of" inurl:"{self.input}/ftp"',

        # Documentos de Projetos
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"projeto" filetype:pdf OR filetype:doc OR filetype:ppt',

        # Certificados
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"certificado" filetype:pdf OR filetype:doc',
        
        # Documentos de Propostas
        f'https://www.google.com/search?q=inurl:"{self.input}" intext:"proposta" filetype:pdf OR filetype:doc',
        
        # Dados de Clientes
        f'https://www.google.com/search?q=inurl:"{self.input}"intext:"lista de clientes" filetype:csv OR filetype:xls',
        
        # Informações sobre fornecedores
        f'https://www.google.com/search?q=inurl:"{self.input}" intext:"fornecedor" filetype:pdf OR filetype:doc',
        
        # Documentação técnica
        f'https://www.google.com/search?q=inurl:"{self.input}" intext:"documentação" filetype:pdf OR filetype:doc'
    ]
        self.user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Mozilla/5.0 (Linux; Ubuntu; X11; rv:85.0) Gecko/20100101 Firefox/85.0",
        "curl/7.68.0",
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        "PostmanRuntime/7.28.0",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
        "Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko",
        ]
        self.headers = {'User-Agent': random.choice(self.user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Connection': 'keep-alive',
                        'Cross-origin-opener-policy':'same-origin-allow-popups; report-to="gws"'
                        }


    #methodo async para requests
    async def fetch(self) -> None:
        try:
            pattern = r'Sua pesquisa não encontrou nenhum documento correspondente' #responsta do body quand
            # Cria uma sessão HTTP assíncrona com os headers (user agent)
            async with aiohttp.ClientSession(headers=self.headers) as session:
               
                for url in self.urls:
                    # Realiza a requisição GET à URL
                    async with session.get(url) as response:
                        # Verifica se a resposta foi bem-sucedida (status 200)
                        if response.status == 200:
                            # Lê o corpo da resposta como texto
                            html = await response.text()
                            
                            if not re.search(pattern, html):
                                # Exibe o URL se houver resultado relevante
                                print(f"{url}")
                                
                        elif response.status == 429:
                            await asyncio.sleep(10) 
                        else:
                            # Exibe uma mensagem de erro com o código de status, se a requisição falhar
                            return(f"Failed to retrieve data. Status code: {response.status}")
                await asyncio.sleep(random.uniform(1, 10))
        except Exception as e:
                # Captura e exibe exceçoes
                print(f'Erro: {e}')
