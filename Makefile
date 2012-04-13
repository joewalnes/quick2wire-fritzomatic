# Run locally
run:
	PYTHONPATH=. DEBUG=1 foreman start
.PHONY: run

# Push site live. You need to have access to the Heroku account.
live:
	git push git@heroku.com:fritzomatic.git
	@echo Pushed to http://fritzomatic.quick2wire.com/
.PHONY: live
