# Run locally
run:
	PYTHONPATH=. foreman start
.PHONY: live

# Push site live. You need to have access to the Heroku account.
live:
	git push git@heroku.com:fritzomatic.git
	@echo Pushed to http://fritzomatic.quick2wire.com/
.PHONY: live
