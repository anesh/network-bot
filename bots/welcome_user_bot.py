import json
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
    CardFactory,
    MessageFactory,
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    Attachment,
    Activity,
    ActivityTypes,
    ActionTypes,
)

from data_models import WelcomeUserState


class WelcomeUserBot(ActivityHandler):
    def __init__(self, user_state: UserState):
        if user_state is None:
            raise TypeError(
                "[WelcomeUserBot]: Missing parameter. user_state is required but None was given"
            )

        self._user_state = user_state

        self.user_state_accessor = self._user_state.create_property("WelcomeUserState")

        self.WELCOME_MESSAGE = """Hello there. Type in 'help' to see in what ways i can help you"""

        self.fqdn_dict = {}

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # save changes to WelcomeUserState after each turn
        #await self._user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Greet when users are added to the conversation.
        Note that all channels do not send the conversation update activity.
        If you find that this bot works in the emulator, but does not in
        another channel the reason is most likely that the channel does not
        send this activity.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(self.WELCOME_MESSAGE)


    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value is not None:
            #print(turn_context.activity.value)
            self.fqdn_dict = turn_context.activity.value
            print(self.fqdn_dict['fqdn'])
            await self.__send_DNS_ANSWER_card(turn_context)

        if turn_context.activity.text:
            text = turn_context.activity.text.lower()
            if text in ("Help", "help"):
                await self.__send_intro_card(turn_context)
            if text in ("DNS", "dns"):
                await self.__send_DNS_card(turn_context)
            if text in ("lookup"):
                await self.__send_DNS_LOOKUP_card(turn_context)

            else:
                await turn_context.send_activity(self.WELCOME_MESSAGE)

    async def __send_intro_card(self, turn_context: TurnContext):

        message = Activity(
            text="Below is a list of Options i can help you with",
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment()],
        )

        await turn_context.send_activity(message)

    async def __send_DNS_card(self, turn_context: TurnContext):

        message = Activity(
            text="Below is a list of DNS Options i can help you with",
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_DNS_attachment()],
        )

        await turn_context.send_activity(message)

    async def __send_DNS_LOOKUP_card(self, turn_context: TurnContext):

        message = Activity(
            text="Input your values in the textfield",
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_DNS_LOOKUP_attachment()],
        )

        await turn_context.send_activity(message)

    async def __send_DNS_ANSWER_card(self, turn_context: TurnContext):

        message = Activity(
            text="DNS Response:",
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_DNS_ANSWER_attachment()],
        )

        await turn_context.send_activity(message)


    def _create_adaptive_card_attachment(self) -> Attachment:

        json_data={
         "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
         "type": "AdaptiveCard",
         "version": "1.0",
         "body": [
          {
        "type": "TextBlock",
        "text": "DNS",
        "size": "medium",
        "weight": "bolder",
          },
          {
        "type": "TextBlock",
        "text": "IPAM",
        "size": "medium",
        "weight": "bolder",
          },
          {
        "type": "TextBlock",
        "text": "Load Balancing",
        "size": "medium",
        "weight": "bolder",
          },
          {
        "type": "TextBlock",
        "text": "Network",
        "size": "medium",
        "weight": "bolder",
          },

         ]
      
        }

        in_file = json.dumps(json_data)
 
        card_data = json.loads(in_file)
        return CardFactory.adaptive_card(card_data)

    def _create_adaptive_DNS_attachment(self) -> Attachment:

        json_data={
         "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
         "type": "AdaptiveCard",
         "version": "1.0",
         "body": [
          {
        "type": "TextBlock",
        "text": "lookup",
        "size": "medium",
        "weight": "bolder",
          },

         ]

        }

        in_file = json.dumps(json_data)
 
        card_data = json.loads(in_file)
        return CardFactory.adaptive_card(card_data)

    def _create_adaptive_DNS_LOOKUP_attachment(self) -> Attachment:

        json_data={
         "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
         "type": "AdaptiveCard",
         "version": "1.0",
         "body": [
            {
            "type": "TextBlock",
            "text": "FQDN/NAME",
            "wrap": "true"
            },
            {
            "type": "Input.Text",
            "style": "text",
            "id": "fqdn"
           },

         ],
         "actions":[
          {
           "type":"Action.Submit",
           "Title": "lookup"

          }
        
        ]

        }

        in_file = json.dumps(json_data)

        card_data = json.loads(in_file)
        return CardFactory.adaptive_card(card_data)

    def _create_adaptive_DNS_ANSWER_attachment(self) -> Attachment:

        json_data={
         "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
         "type": "AdaptiveCard",
         "version": "1.0",
         "body": [
          {
        "type": "TextBlock",
        "text": self.fqdn_dict['fqdn'],
        "size": "medium",
        "weight": "bolder",
          },

         ]

        }

        in_file = json.dumps(json_data)
 
        card_data = json.loads(in_file)
        return CardFactory.adaptive_card(card_data)

