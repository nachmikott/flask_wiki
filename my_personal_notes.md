The Code As Is:
* Validators as Decorators:
--> Situation: Currently, I have validators that are called at the Wikipedia_API Helper level. These validators are called like regular methods, but they are applicable to multiple Views. Where the validators are now seems to deep in the application, and should be bubbled up, so as to maintain a _fail-fast_ response in our code-base as well as seperation of duties (app or blueprint layer should handle validations and exceptions, let the Wikipedia_API Helper deal with calling the Wikipedia Article API!)
--> Options:
   * DIY --> Create our own validator functions, and just use them as decorators in our views.
   * Adopt a RESTFul API as a first-class-objective, which will have a built-in validation architecture.
   * Adopt a Validator mechanism from a third-party resource.
      * Ex/ https://marshmallow.readthedocs.io/en/stable/index.html 
      * Pros: Has built-in validations, especially with dates.
      * Cons: Is pretty baked into Marshmallows larger ecosystem/architecture. May need to consider a new Serialization/Deserialization mechanism beyond json.load/dump as we do now. That is additional overhead unrelated to validations. Would have to adopt mashmallows Schema patterns.
* Logging/Telemetry to/from Libraries/3rd Parties
--> Situation: Currently, I have print logs only by the Exceptions. There are lots of opportunities to improve this! Consider APM (Application Performance Monitoring).
--> Ideas: 
    - Events
        * Events should be created in a way that allows for Tracing (on a particular app, on a particular session, on a particular server?)
        * This could be done for example using OpenTelemetrySDK, and an OpenTelemetry Collector, in conjunction with ElasticStack or other log aggregator.

* Leveraging Exception Handler Registration instead of so much try/catch codeblocks.
--> Situation: Currently, I have a long try/catch block in each of the Views. Long/Nested Try/Catch Blocks can become combersome to maintain, and involves lots of boilerplate code.
--> There is an opportunity to collocate all of our exception types, but with specific details _per request_.
--> There are many ways to do this, but through more research, I have found that Flask offers exception handler registration via a decorator _on the app_ layer. I did not leverage Blueprints in this setup, so for now, our registrations should be _on the app_ layer. But if we create the registrations modularly/functionaly, we should be able to use  the same code/tests when/if we migrate over to Blueprints.
   * flask_app.register_error_handler(some_code, handle_bad_request)
      * handle_bad_request is a function that returns a tuple of (status_code, exception_info).
   * we would still need to raise exceptions within code, but no longer have long try/catches! (and collocate exceptions with logging).

* Improved Colocation of Code and Documentation (Especially for the Swagger UI).

* Better Handling of Improper Routes & Rerouting Opportunities


-------- Other Ideas: ------------------------------------------------------------------------------------
Interactions with Downstream Services:
* Consider Error Handling and BackOff For Calling the Wikipedia API?
* Maintaining Versioning and Staging Environment Of Downstream Services Through Configuration
* Version Modeling to Python Class Object?

Interactions with Engineers:
* Engineers Who Contribute
* Engineers Who Write Code That Wants To Use REST API Endpoint

Interactions with Upstream Services (Users):
* Throttling Considerations
* Response Code Considerations
* Secure Transfer Considerations;
    * API Key Authorization
* SLA Considerations:
    * On Average, how long to wait before timingout?
    * CAP <-- Which Two? Consistency is difficult to determine at this layer as we don't access the DB on our own, Wikipedia API Does that.

Deployment Strategies:
* Infrastrcuture As Code:
* Load Balancing
* Auto Scaling
* Dockerized Deployment, to ensure a stable/deterministic environment, whichever host provider decided.


