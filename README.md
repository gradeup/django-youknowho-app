# django-youknowho-app

Youknowwho Gui is a Django app to give gui for [rule-engine](https://github.com/gradeup/youknowwho) app. It provides an api to get rules in a format easily readable by rule engine.
A interface is also bundled with using which one can simulate rules.

## Installation

* Download and install manually

```
git clone https://github.com/gradeup/youknowho-gui.git
cd youknowho-gui
python setup.py install
```

## Use

1. Add "youknowwhogui" to your INSTALLED_APPS like this

```
INSTALLED_APPS = (
    ...
    'youknowwhogui',
)
```

2. To create models, run migrate like

```
python manage.py migrate
```

3. Include the urls of the app in your root url by

```
url(r'^youknowwhogui/', include('youknowwhogui.urls', namespace='youknowwhogui')),
```

4. To get the list of all rules, in json format, use `/rules` api. Assuming that your app is running at port 8000, rules can be accessed by [http://localhost:8000/youknowwhogui/rules](http://localhost:8000/youknowwhogui/rules)

5. Simulation Interface can be accessed at `simulate` endpoint. If app is running at port 8000, it can be accessed by [http://localhost:8000/youknowwhogui/simulate](http://localhost:8000/youknowwhogui/simulate).

6. Simulation panel depends on the node application which is running an instance of [youknowwho](https://github.com/gradeup/youknowwho). A get api needs to be exposed in this app, so that the django app can connect and display the output. This all can be configured by specifying by following variables in django project settings

* RULE_ENGINE_SIMULATION_URL

* RULE_ENGINE_SIMULATION_API_ENDPOINT

* RULE_ENGINE_X_CLIENT_ID (to identify requests from simulation interface)

## Snapshots

#### Overview

A django admin view of one rule. This rule checks if the number is positive and sets a key of _sign_

![rule-positive-sign](https://github.com/gradeup/youknowwho-gui/blob/master/.snaps/re-admin-view.png "Rule Engine Check positive rule view")

![rule-positive-sign-other](https://github.com/gradeup/youknowwho-gui/blob/master/.snaps/re-admin-other-view.png "Rule Engine Check positive rule view")

#### Overall View

![re-sim-overall](https://github.com/gradeup/youknowwho-gui/blob/master/.snaps/re-sim-overall.png "Rule Engine Simulation Overall View")

#### Rules wise view

Rules which are applied are shown in green color and rules which are not applied are shown in red color.

![re-sim-applied-rules-view](https://github.com/gradeup/youknowwho-gui/blob/master/.snaps/re-sim-applied-rules-view.png "Rule Engine Simulation Rules Applied View")
![re-sim-not-applied-rules](https://github.com/gradeup/youknowwho-gui/blob/master/.snaps/re-sim-not-applied-rules.png "Rule Engine Simulation Rules Not Applied View")
