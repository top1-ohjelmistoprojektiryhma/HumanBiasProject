# Arkkitehtuuri

## Rakenne

Sovelluksen rakennetta kuvaa pakkausrakenne:

![Pakkauskaavio](./kuvat/pakkauskaavio.drawio.png)

_UI_ sisältää selainkäyttöliittymän koodin. _Services_ sisältää sovelluslogiikan koodin ja erikseen kutsuu _API_-pakkauksen kielimallikutsuista vastaavia luokkia.

## Sovelluslogiikka

Sovelluslogiikan muodostavat logiikkaluokka Service handler ja session manager -luokka, jotka hoitavat Api manager ja Agent manager -luokkien toimintaa. Dialog luokka hoitaa mm. formatointia valitun formaatin mukaan:

```mermaid
classDiagram
   ServiceHandler ..> SessionManager
   ServiceHandler ..> ApiManager
   ServiceHandler ..> AgentManager
   SessionManager ..> Dialog
   class SessionManager{
    new_session
    get_session_prompts
    update_session
   }
   class ServiceHandler{
    start_new_session
    continue_session
    generate_agents
    getsummary_from_AI
   }
  class ApiManager {
    sendp_rompts
   }
  class AgentManager {
    add_agent
    delete_agent
    set_selected_agents
   }
  class Dialog {
    initial_prompts
    get_prompts
    update_with_responses
}

```

## Päätoiminnallisuudet

### Syötteen ja formaatin valitseminen

Sovelluksen etusivulla voi syöttää tulevaisuusväittämän itse tai lisätä tiedoston (txt, pdf, docx, odt). Seuraavassa vaiheessa _next_-napin painalluksen jälkeen käyttäjä voi valita formaatin. Formaatit ovat _dialog-no-consensus_, _dialog-consensus_ ja _bias-finder_.

### Uuden dialogin aloittaminen

Kun käyttäjä on syöttäny aloitusväittämän tai -tiedoston, etenee sovelluksen toiminta seuraavasti:

```mermaid
sequenceDiagram
   actor User
   User->>UI: click "Submit" button
   UI->>ServiceHandler: start_new_session()
   Activate ServiceHandler
   ServiceHandler->>SessionManager: new_session()
   Activate SessionManager
   SessionManager->>Dialog: __init__()
   Activate Dialog
   Dialog->>SessionManager: Dialog
   Deactivate Dialog
   SessionManager-->>ServiceHandler: Dialog, session_id
   Deactivate SessionManager
   ServiceHandler->>SessionManager: get_session_prompts()
   Activate SessionManager
   SessionManager->>Dialog: get_prompts()
   Dialog-->>SessionManager: api_input_list
   SessionManager-->>ServiceHandler: prompts
   Deactivate SessionManager
   ServiceHandler->>ApiManager: send_prompts(propmts)
   Activate ApiManager
   ApiManager->>API: get_response()
   API-->>ApiManager: response
   ApiManager-->>ServiceHandler: response
   Deactivate ApiManager
   ServiceHandler->>SessionManager: update_session_with_responsenes(response)
   Activate SessionManager
   SessionManager->>Dialog: update_with_responses(response)
   ServiceHandler->>SessionManager: get_session(session_id).to_dict()
   Activate SessionManager
   SessionManager->>Dialog: to_dict()
   Dialog-->>SessionManager: dict(Dialog)
   SessionManager-->>ServiceHandler: dict(Dialog)
   Deactivate SessionManager
   ServiceHandler-->>UI: "success", dict(Dialog)
   Deactivate ServiceHandler
```

### Dialogin jatkaminen

Sovelluksessa voi edellisen kohdan jälkeen jatkaa "keskustelua" painamalla _continue_ -näppäintä. Sovelluksen toiminta jatkuu silloin samalla tavalla, kuin aloituksen dialogin luomisen jälkeen.

### Dialogin lopettaminen

Sovelluksessa voi "keskustelun" lopettaa painamalla _stop_-näppäintä. Tällöin sovellus palaa alkutilaan, josta voi aloittaa uuden dialogin ja valita formaatin.
