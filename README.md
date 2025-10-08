# 📚 Biblioteca Digital de Artigos

Este projeto tem como objetivo desenvolver uma **biblioteca digital** para disponibilizar **acesso fácil e centralizado aos artigos publicados** em determinados eventos científicos. A plataforma será um repositório organizado, permitindo que usuários encontrem e acessem produções acadêmicas de forma eficiente.

Inspirado em plataformas consagradas como a **ACM Digital Library** e a **SBC Open-Lib**, nosso objetivo é criar uma ferramenta robusta para a comunidade acadêmica, facilitando a disseminação do conhecimento científico.

---

## ✨ Funcionalidades Principais

A plataforma conta com um conjunto completo de funcionalidades para administradores e usuários:

- **Gerenciamento de Conteúdo:** Administradores podem cadastrar, editar e remover **eventos, edições e artigos** através de uma interface de administração intuitiva.
- **Importação em Massa:** Suporte para **cadastro de múltiplos artigos de uma só vez** a partir de um arquivo no formato **BibTeX**, agilizando a alimentação do sistema.
- **Busca Avançada:** Usuários podem realizar buscas por **título do artigo, autor ou nome do evento**, encontrando a informação que precisam de forma rápida.
- **Páginas Personalizadas:** Cada evento possui uma página dedicada que lista suas edições, e cada edição lista os artigos correspondentes, criando uma navegação lógica e hierárquica.
- **Área do Usuário:** Usuários registrados possuem uma página pessoal ("Meus Artigos") que organiza os artigos que submeteram, agrupados por ano.
- **Sistema de Notificações:** Os usuários podem se inscrever para receber **notificações por e-mail** sempre que um novo artigo com palavras-chave de seu interesse for publicado.
- **Interface Moderna:** O sistema conta com um **tema claro e escuro (dark mode)**, tanto no site principal quanto no painel de administração, para uma experiência de uso mais confortável.

---

## 👥 Membros da Equipe e Papéis

| Nome | Matrícula | Papel |
|--------------|------------|-----------|
| Joao Vitor Gomes Mapa da Silva | 2019027695 | Fullstack |
| Luis Henrique Ribeiro Maciel | 2021020759 | Fullstack |
| Seungbin Han | 2025550850 | Fullstack |
| Leonardo Bhering Damasceno | 2020006728 | Fullstack |

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.12
- **Backend**: Django 5.2
- **Frontend**: HTML + CSS (com Tailwind CSS via CDN)
- **Banco de Dados**: SQLite
- **Agente IA**: Cursor e Gemini

---

## 🚀 Como Executar o Projeto

As instruções detalhadas para configurar o ambiente de desenvolvimento, instalar as dependências e executar o projeto localmente estão disponíveis no arquivo **[how2run.md](./how2run.md)**.

---

## 📌 Backlog do Produto

- **[CONCLUÍDO]** Como administrador, eu quero cadastrar, editar e deletar um evento.
- **[CONCLUÍDO]** Como administrador, eu quero cadastrar, editar e deletar uma nova edição de um evento.
- **[CONCLUÍDO]** Como administrador, eu quero cadastrar, editar e deletar um artigo manualmente, incluindo seu PDF.
- **[CONCLUÍDO]** Como administrador, eu quero cadastrar artigos em massa a partir de um arquivo BibTeX.
- **[CONCLUÍDO]** Como usuário, eu quero pesquisar artigos por título, autor e nome do evento.
- **[CONCLUÍDO]** Como administrador, eu quero que todo evento tenha uma home page com suas edições, e que cada edição tenha uma home page com seus artigos.
- **[CONCLUÍDO]** Como usuário, eu quero ter uma home page com os meus artigos, organizados por ano.
- **[CONCLUÍDO]** Como usuário, eu quero me cadastrar para receber um e-mail sempre que um novo artigo de meu interesse for disponibilizado.

---

## 📆 Backlog da Sprint

### História 1: Como administrador, eu quero cadastrar, editar e deletar um evento e suas edições.
- Criar os modelos de dados `Event` e `Edition` com seus respectivos campos e relacionamentos. – **[Membro]**
- Registrar os modelos no painel de administração (`admin.py`) para permitir o gerenciamento via interface. – **[Membro]**
- Criar as views e templates para a listagem pública (`event_list`) e detalhamento (`event_detail`) dos eventos. – **[Membro]**
- Criar as views e templates para a detalhamento (`edition_detail`) das edições. – **[João Vitor]**

### História 2: Como usuário, eu quero pesquisar artigos por título, autor e nome do evento.
- Implementar a barra de busca no `base.html` e direcionar para a URL de busca. – **[Membro]**
- Criar a view `article_search_view` no backend, contendo a lógica de consulta com `Q objects` para buscar em múltiplos campos. – **[Membro]**
- Criar o template `article_search_results.html` para exibir os resultados da busca de forma clara para o usuário. – **[Membro]**

### História 3: Como usuário, eu quero ter uma home page com os meus artigos, organizados por ano.
- Implementar a view `my_articles_view`, protegida por `@login_required`, para filtrar artigos pelo `request.user`. – **[Membro]**
- Adicionar a lógica de programação para agrupar os artigos em um dicionário onde as chaves são os anos. – **[Membro]**
- Criar o template `my_articles.html` com loops aninhados para renderizar os artigos agrupados por ano. – **[Membro]**
- Adicionar o link "Meus Artigos" no menu do usuário no `base.html`. – **[João Vitor]**

### História 4: Como administrador, eu quero cadastrar artigos em massa a partir de um arquivo BibTeX.
- Implementar a view `bulk_upload_view` no `ArticleAdmin` para processar o upload do arquivo. – **[João Vitor]**
- Adicionar a lógica de parsing do arquivo `.bib` usando a biblioteca `bibtexparser`. – **[João Vitor]**
- Implementar a lógica "get or create" para encontrar ou criar `Eventos` e `Edições` com base nos dados do arquivo. – **[João Vitor]**
- Criar os templates customizados do admin (`change_list.html` e `bulk_upload.html`) para exibir o botão e a página de upload. – **[João Vitor]**
