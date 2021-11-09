import responses
from django.test import TestCase, override_settings

from chains.models import Feature, Wallet
from chains.tests.factories import ChainFactory


@override_settings(
    CGW_URL="http://127.0.0.1",
    CGW_FLUSH_TOKEN="example-token",
)
class ChainNetworkHookTestCase(TestCase):
    @responses.activate
    def test_on_chain_update_hook_200(self) -> None:
        responses.add(
            responses.POST,
            "http://127.0.0.1/v1/flush/example-token",
            status=200,
            match=[responses.matchers.json_params_matcher({"invalidate": "Chains"})],  # type: ignore[no-untyped-call]
        )

        ChainFactory.create()

        assert len(responses.calls) == 1
        assert responses.calls[0].request.body == b'{"invalidate": "Chains"}'
        assert (
            responses.calls[0].request.url == "http://127.0.0.1/v1/flush/example-token"
        )

    @responses.activate
    def test_on_chain_update_hook_400(self) -> None:
        responses.add(
            responses.POST,
            "http://127.0.0.1/v1/flush/example-token",
            status=400,
            match=[responses.matchers.json_params_matcher({"invalidate": "Chains"})],  # type: ignore[no-untyped-call]
        )

        ChainFactory.create()

        assert len(responses.calls) == 1

    @responses.activate
    def test_on_chain_update_hook_500(self) -> None:
        responses.add(
            responses.POST,
            "http://127.0.0.1/v1/flush/example-token",
            status=500,
            match=[responses.matchers.json_params_matcher({"invalidate": "Chains"})],  # type: ignore[no-untyped-call]
        )

        ChainFactory.create()

        assert len(responses.calls) == 1

    @responses.activate
    def test_on_chain_delete_hook_call(self) -> None:
        chain = ChainFactory.create()

        chain.delete()

        # 2 calls: one for creation and one for deletion
        assert len(responses.calls) == 2

    @responses.activate
    def test_on_chain_update_hook_call(self) -> None:
        chain = ChainFactory.create()

        # Not updating using queryset because hooks are not triggered that way
        chain.currency_name = "Ether"
        chain.save()

        # 2 calls: one for creation and one for updating
        assert len(responses.calls) == 2

    @override_settings(
        CGW_URL=None,
        CGW_FLUSH_TOKEN=None,
    )
    @responses.activate
    def test_on_chain_update_with_no_cgw_set(self) -> None:
        ChainFactory.create()

        assert len(responses.calls) == 0

    @override_settings(
        CGW_URL="http://127.0.0.1",
        CGW_FLUSH_TOKEN=None,
    )
    @responses.activate
    def test_on_chain_update_with_no_flush_token_set(self) -> None:
        ChainFactory.create()

        assert len(responses.calls) == 0


@override_settings(
    CGW_URL="http://127.0.0.1",
    CGW_FLUSH_TOKEN="example-token",
)
class FeatureHookTestCase(TestCase):
    @responses.activate
    def test_on_feature_create_hook_call(self) -> None:
        responses.add(
            responses.POST,
            "http://127.0.0.1/v1/flush/example-token",
            status=200,
            match=[responses.matchers.json_params_matcher({"invalidate": "Chains"})],  # type: ignore[no-untyped-call]
        )

        Feature(key="Test Feature").save()

        assert len(responses.calls) == 1
        assert responses.calls[0].request.body == b'{"invalidate": "Chains"}'
        assert (
            responses.calls[0].request.url == "http://127.0.0.1/v1/flush/example-token"
        )

    @responses.activate
    def test_on_feature_delete_hook_call(self) -> None:
        feature = Feature(key="Test Feature")

        feature.save()  # create
        feature.delete()  # delete

        # 2 calls: one for creation and one for deletion
        assert len(responses.calls) == 2

    @responses.activate
    def test_on_feature_update_hook_call(self) -> None:
        feature = Feature(key="Test Feature")

        feature.save()  # create
        feature.key = "New Test Feature"
        feature.save()  # update

        # 2 calls: one for creation and one for updating
        assert len(responses.calls) == 2


@override_settings(
    CGW_URL="http://127.0.0.1",
    CGW_FLUSH_TOKEN="example-token",
)
class WalletHookTestCase(TestCase):
    @responses.activate
    def test_on_wallet_create_hook_call(self) -> None:
        responses.add(
            responses.POST,
            "http://127.0.0.1/v1/flush/example-token",
            status=200,
            match=[responses.matchers.json_params_matcher({"invalidate": "Chains"})],  # type: ignore[no-untyped-call]
        )

        Wallet(name="Test Wallet").save()

        assert len(responses.calls) == 1
        assert responses.calls[0].request.body == b'{"invalidate": "Chains"}'
        assert (
            responses.calls[0].request.url == "http://127.0.0.1/v1/flush/example-token"
        )

    @responses.activate
    def test_on_wallet_delete_hook_call(self) -> None:
        wallet = Wallet(name="Test Wallet")

        wallet.save()  # create
        wallet.delete()  # delete

        # 2 calls: one for creation and one for deletion
        assert len(responses.calls) == 2

    @responses.activate
    def test_on_wallet_update_hook_call(self) -> None:
        wallet = Wallet(name="Test Wallet")

        wallet.save()  # create
        wallet.name = "Test Wallet v2"
        wallet.save()  # update

        # 2 calls: one for creation and one for updating
        assert len(responses.calls) == 2
