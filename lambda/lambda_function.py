# -*- coding: utf-8 -*-

# This is a sample of an Alexa skill using the Alexa Skills Kit SDK for Python.
# ADD GITHUB SOURCE HERE

import logging
import json
import random

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream, AudioItemMetadata,
    StopDirective, ClearQueueDirective, ClearBehavior)

# Initializing the logger and setting the level to "INFO"
# Read more about it here https://www.loggly.com/ultimate-guide/python-logging-basics/
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Audio stream metadata
STREAMS = [
  {
    "token": '1',
    "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/album+free+your+mind+-+by+Master+Minded+-+song+Opening+Up.mp3',
    "metadata": {
      "title": 'Opening up by Mastermind',
      "subtitle": 'Album Free your mind',
      "art": {
        "sources": [
          {
            "contentDescription": 'Album: Free your mind',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/album+free+your+mind+-+by+Master+Minded+-+song+Opening+Up.jpeg',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": 'my room',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/NightBackground01.jpg',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  },
  {
    "token": '2',
    "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/album+Ludicity+by+Onyx+Music-+song+Blue+Dream.mp3',
    "metadata": {
      "title": 'Blue Dream by Onyx Music',
      "subtitle": 'Album Ludicity',
      "art": {
        "sources": [
          {
            "contentDescription": 'Album: Ludicity',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/album+Ludicity+by+Onyx+Music-+song+Blue+Dream.jpeg',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": 'example image',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/NightBackground01.jpg',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  },
  {
    "token": '3',
    "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/by+Okaya+-+album+Dreaming+of+Peace+-+song+No+Backing+Vocals.mp3',
    "metadata": {
      "title": 'No Backing Vocals by Okaya',
      "subtitle": 'Album Dreaming of Peace',
      "art": {
        "sources": [
          {
            "contentDescription": 'Album: Dreaming of Peace',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/by+Okaya+-+album+Dreaming+of+Peace+-+song+No+Backing+Vocals.jpg',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": 'my room',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/NightBackground01.jpg',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  },
  {
    "token": '4',
    "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/Field+Album+by+Tamuz+Dekel+-+song+Evanescent.mp3',
    "metadata": {
      "title": 'Evanescent by Tamuz Dekel',
      "subtitle": 'Album Field',
      "art": {
        "sources": [
          {
            "contentDescription": 'Album: Field',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/Field+Album+by+Tamuz+Dekel+-+song+Evanescent.jpg',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": 'my room',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/NightBackground01.jpg',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  },
  {
    "token": '5',
    "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/Still+Mootion+Album+by+Adi+Goldstein+-+song+Fireflies.mp3',
    "metadata": {
      "title": 'Fireflies by Adi Goldstein',
      "subtitle": 'Album Still Mootion',
      "art": {
        "sources": [
          {
            "contentDescription": 'Album: Still Mootiont',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/Still+Mootion+Album+by+Adi+Goldstein+-+song+Fireflies.jpeg',
            "widthPixels": 512,
            "heightPixels": 512
          }
        ]
      },
      "backgroundImage": {
        "sources": [
          {
            "contentDescription": 'my room',
            "url": 'https://streamfiletest.s3.us-east-1.amazonaws.com/testaudiofile/NightBackground01.jpg',
            "widthPixels": 1200,
            "heightPixels": 800
          }
        ]
      }
    }
  }
]

# Intent Handlers

# This handler checks if the device supports audio playback
class CheckAudioInterfaceHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        if handler_input.request_envelope.context.system.device:
            return handler_input.request_envelope.context.system.device.supported_interfaces.audio_player is None
        else:
            return False

    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = language_prompts["DEVICE_NOT_SUPPORTED"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )

# This handler starts the stream playback whenever a user invokes the skill or resumes playback.
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self,handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .speak("Starting {}".format(stream["metadata"]["title"]))
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )

class ResumeStreamIntentHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return (is_request_type("PlaybackController.PlayCommandIssued")(handler_input)
                or is_intent_name("AMAZON.ResumeIntent")(handler_input)
                )
    def handle(self,handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )

# This handler handles all the required audio player intents which are not supported by the skill yet. 
class PreviousNextIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.NextIntent")(handler_input)
                or is_intent_name("AMAZON.PreviousIntent")(handler_input)
                or is_intent_name("AMAZON.StartOverIntent")(handler_input)
                )

    def handle(self, handler_input):
        intent_name = handler_input.request_envelope.request.intent.name

        if intent_name == "AMAZON.NextIntent":
            return self.handle_next_intent(handler_input)
        elif intent_name == "AMAZON.PreviousIntent":
            return self.handle_previous_intent(handler_input)
        elif intent_name == "AMAZON.StartOverIntent":
            return self.handle_start_over_intent(handler_input)
        else:
            language_prompts = handler_input.attributes_manager.request_attributes["_"]
            speech_output = random.choice(language_prompts["UNHANDLED"])
            return (
                handler_input.response_builder
                    .speak(speech_output)
                    .set_should_end_session(True)
                    .response
            )

    def get_current_index(self, token):
        for index, stream in enumerate(STREAMS):
            if stream["token"] == token:
                return index
        return 0

    def handle_next_intent(self, handler_input):
        # Logic to handle NextIntent
        current_token = handler_input.request_envelope.context.audio_player.token
        current_index = self.get_current_index(current_token)
        next_index = current_index + 1

        if next_index >= len(STREAMS):
            speech_output = "This is the last song."
            stream = STREAMS[current_index]
        else:
            speech_output = "Playing next song: {}".format(STREAMS[next_index]["metadata"]["title"])
            stream = STREAMS[next_index]

        return (
            handler_input.response_builder
                .speak(speech_output)
                .add_directive(
                    PlayDirective(
                        play_behavior=PlayBehavior.REPLACE_ALL,
                        audio_item=AudioItem(
                            stream=Stream(
                                token=stream["token"],
                                url=stream["url"],
                                offset_in_milliseconds=0,
                                expected_previous_token=None),
                            metadata=stream["metadata"]
                        )
                    )
                )
                .set_should_end_session(True)
                .response
        )

    def handle_previous_intent(self, handler_input):
        # Logic to handle PreviousIntent
        current_token = handler_input.request_envelope.context.audio_player.token
        current_index = self.get_current_index(current_token)
        previous_index = current_index - 1

        if previous_index < 0:
            speech_output = "This is the first song."
            stream = STREAMS[current_index]
        else:
            speech_output = "Playing previous song: {}".format(STREAMS[previous_index]["metadata"]["title"])
            stream = STREAMS[previous_index]

        return (
            handler_input.response_builder
                .speak(speech_output)
                .add_directive(
                    PlayDirective(
                        play_behavior=PlayBehavior.REPLACE_ALL,
                        audio_item=AudioItem(
                            stream=Stream(
                                token=stream["token"],
                                url=stream["url"],
                                offset_in_milliseconds=0,
                                expected_previous_token=None),
                            metadata=stream["metadata"]
                        )
                    )
                )
                .set_should_end_session(True)
                .response
        )

    def handle_start_over_intent(self, handler_input):
        # Logic to handle StartOverIntent
        current_token = handler_input.request_envelope.context.audio_player.token
        current_index = self.get_current_index(current_token)
        stream = STREAMS[current_index]
        return (
            handler_input.response_builder
                .speak("Starting over: {}".format(stream["metadata"]["title"]))
                .add_directive(
                    PlayDirective(
                        play_behavior=PlayBehavior.REPLACE_ALL,
                        audio_item=AudioItem(
                            stream=Stream(
                                token=stream["token"],
                                url=stream["url"],
                                offset_in_milliseconds=0,
                                expected_previous_token=None),
                            metadata=stream["metadata"]
                        )
                    )
                )
                .set_should_end_session(True)
                .response
        )


# This handler handles all the required audio player intents which are not supported by the skill yet. 
class UnhandledFeaturesIntentHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return (is_intent_name("AMAZON.LoopOnIntent")(handler_input)
                or is_intent_name("AMAZON.ShuffleOnIntent")(handler_input)
                or is_intent_name("AMAZON.ShuffleOffIntent")(handler_input)
                or is_intent_name("AMAZON.LoopOffIntent")(handler_input)
                )
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["UNHANDLED"])
        return (
            handler_input.response_builder
                .speak(speech_output)
                .set_should_end_session(True)
                .response
            )
    
    
# This handler handles the repeat intent.     
class RepeatIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        current_token = handler_input.request_envelope.context.audio_player.token
        current_index = self.get_current_index(current_token)
        stream = STREAMS[current_index]
        
        speech_output = "Playing song: {}".format(stream["metadata"]["title"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .add_directive(
                    PlayDirective(
                        play_behavior=PlayBehavior.REPLACE_ALL,
                        audio_item=AudioItem(
                            stream=Stream(
                                token=stream["token"],
                                url=stream["url"],
                                offset_in_milliseconds=0,
                                expected_previous_token=None),
                            metadata=stream["metadata"]
                        )
                    )
                )
                .set_should_end_session(True)
                .response
        )

    def get_current_index(self, token):
        for index, stream in enumerate(STREAMS):
            if stream["token"] == token:
                return index
        return 0
        
    
# This handler provides the user with basic info about the skill when a user asks for it.
# Note: This would only work with one shot utterances and not during stream playback.
class AboutIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AboutIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = random.choice(language_prompts["ABOUT"])
        reprompt = random.choice(language_prompts["ABOUT_REPROMPT"])
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["HELP"])
        reprompt = random.choice(language_prompts["HELP_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            is_intent_name("AMAZON.CancelIntent")(handler_input)
            or is_intent_name("AMAZON.StopIntent")(handler_input)
            or is_intent_name("AMAZON.PauseIntent")(handler_input)
            or is_intent_name("AMAZON.NavigateHomeIntent")(handler_input)
            or is_intent_name("AMAZON.FallbackIntent")(handler_input)
            )
    
    def handle(self, handler_input):
        return ( handler_input.response_builder
                    .add_directive(
                        ClearQueueDirective(
                            clear_behavior=ClearBehavior.CLEAR_ALL)
                        )
                    .add_directive(StopDirective())
                    .speak("Goodbye!")
                    .set_should_end_session(True)
                    .response
                )

class PlaybackStartedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackStarted")(handler_input)
    
    def handle(self, handler_input):
        return ( handler_input.response_builder
                    .add_directive(
                        ClearQueueDirective(
                            clear_behavior=ClearBehavior.CLEAR_ENQUEUED)
                        )
                    .response
                )

class PlaybackStoppedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ( is_request_type("PlaybackController.PauseCommandIssued")(handler_input)
                or is_request_type("AudioPlayer.PlaybackStopped")(handler_input)
            )
    
    def handle(self, handler_input):
        return ( handler_input.response_builder
                    .add_directive(
                        ClearQueueDirective(
                            clear_behavior=ClearBehavior.CLEAR_ALL)
                        )
                    .add_directive(StopDirective())
                    .set_should_end_session(True)
                    .response
                )

# This handler tries to play the stream again if the playback failed due to any reason.
class PlaybackFailedIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("AudioPlayer.PlaybackFailed")(handler_input)
    
    def handle(self,handler_input):
        stream = STREAMS[0]
        return ( handler_input.response_builder
                    .add_directive(
                        PlayDirective(
                            play_behavior=PlayBehavior.REPLACE_ALL,
                            audio_item=AudioItem(
                                stream=Stream(
                                    token=stream["token"],
                                    url=stream["url"],
                                    offset_in_milliseconds=0,
                                    expected_previous_token=None),
                                metadata=stream["metadata"]
                            )
                        )
                    )
                    .set_should_end_session(True)
                    .response
                )
    

# This handler handles utterances that can't be matched to any other intent handler.
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        speech_output = random.choice(language_prompts["FALLBACK"])
        reprompt = random.choice(language_prompts["FALLBACK_REPROMPT"])
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class ExceptionEncounteredRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("System.ExceptionEncountered")(handler_input)
    
    def handle(self, handler_input):
        logger.info("Session ended with reason: {}".format(handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response

# Interceptors

# This interceptor is used for supporting different languages and locales. It detects the users locale,
# loads the corresponding language prompts and sends them as a request attribute object to the handler functions.
class LocalizationInterceptor(AbstractRequestInterceptor):

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        
        try:
            with open("languages/"+str(locale)+".json") as language_data:
                language_prompts = json.load(language_data)
        except:
            with open("languages/"+ str(locale[:2]) +".json") as language_data:
                language_prompts = json.load(language_data)
        
        handler_input.attributes_manager.request_attributes["_"] = language_prompts

# This interceptor logs each request sent from Alexa to our endpoint.
class RequestLogger(AbstractRequestInterceptor):

    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

# This interceptor logs each response our endpoint sends back to Alexa.
class ResponseLogger(AbstractResponseInterceptor):

    def process(self, handler_input, response):
        logger.debug("Alexa Response: {}".format(response))

# This exception handler handles syntax or routing errors. If you receive an error stating 
# the request handler is not found, you have not implemented a handler for the intent or 
# included it in the skill builder below
class CatchAllExceptionHandler(AbstractExceptionHandler):
    
    def can_handle(self, handler_input, exception):
        return True
    
    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        
        language_prompts = handler_input.attributes_manager.request_attributes["_"]
        
        speech_output = language_prompts["ERROR"]
        reprompt = language_prompts["ERROR_REPROMPT"]
        
        return (
            handler_input.response_builder
                .speak(speech_output)
                .ask(reprompt)
                .response
            )

# Skill Builder
# Define a skill builder instance and add all the request handlers,
# exception handlers and interceptors to it.

sb = SkillBuilder()
sb.add_request_handler(CheckAudioInterfaceHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ResumeStreamIntentHandler())
sb.add_request_handler(PreviousNextIntentHandler())
sb.add_request_handler(UnhandledFeaturesIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(PlaybackStartedIntentHandler())
sb.add_request_handler(PlaybackStoppedIntentHandler())
sb.add_request_handler(PlaybackFailedIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

lambda_handler = sb.lambda_handler()
