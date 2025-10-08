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

## 📆 Backlog da Sprint (Exemplo de Divisão de Tarefas)

### História 1: Gerenciamento de Conteúdo (Eventos, Edições e Artigos)
- Criar modelos de dados para `Event`, `Edition` e `Article`. – **[Feito]**
- Registrar modelos no painel de administração do Django. – **[Feito]**
- Criar views e templates para a listagem e detalhamento de eventos e edições. – **[Feito]**

### História 2: Funcionalidades de Usuário (Cadastro, Login, Busca e Página Pessoal)
- Configurar o aplicativo `users` para cadastro e autenticação. – **[Feito]**
- Implementar a lógica de busca no backend e a interface no frontend. – **[Feito]**
- Criar a view `my_articles_view` para filtrar artigos por usuário e agrupar por ano. – **[Feito]**
- Implementar o template `my_articles.html`. – **[Feito]**

### História 3: Funcionalidades Avançadas (Importação em Massa e Notificações)
- Implementar a view `bulk_upload_view` no `ArticleAdmin` para processar arquivos BibTeX. – **[Feito]**
- Criar modelo `UserInterest` para armazenar preferências de notificação. – **[Feito]**
- Implementar a página de gerenciamento de interesses para os usuários. – **[Feito]**
- Configurar Sinais do Django (`post_save`) para disparar a lógica de envio de e-mails. – **[Feito]**

### História 4: Melhorias de Interface (UI/UX)
- Implementar modo claro e escuro (dark mode) para o site principal. – **[Feito]**
- Implementar um menu de usuário em formato dropdown. – **[Feito]**
- Implementar modo claro e escuro para o painel de administração do Django. – **[Feito]**
