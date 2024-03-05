class Felt:
    def __init__(self, cairo_obj) -> None:
        self.v = int(cairo_obj)

    def __repr__(self) -> str:
        f"{hex(self.v)}"


class FeltArray:
    def __init__(self, cairo_obj, len) -> None:
        self.v = []
        for i in range(len):
            self.v.append(Felt(cairo_obj[i]))

    def __repr__(self) -> str:
        res = ""
        for i in range(len(self.v)):
            res += f"{self.v[i].__repr__()}\n"


class SegmentInfo:
    def __init__(self, cairo_obj) -> None:
        self.begin_addr = Felt(cairo_obj.begin_addr)
        self.stop_ptr = Felt(cairo_obj.stop_ptr)


class AddrValue:
    def __init__(self, cairo_obj) -> None:
        self.address = Felt(cairo_obj.address)
        self.value = Felt(cairo_obj.value)


class ContinuousPageHeader:
    def __init__(self, cairo_obj) -> None:
        self.start_address = Felt(cairo_obj.start_address)
        self.size = Felt(cairo_obj.size)
        self.hash = Felt(cairo_obj.hash)
        self.prod = Felt(cairo_obj.prod)


class ChannelUnsentFelt:
    def __init__(self, cairo_obj) -> None:
        self.value = Felt(cairo_obj.value)


class ChannelSentFelt:
    def __init__(self, cairo_obj) -> None:
        self.value = Felt(cairo_obj.value)


class StarkUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.traces = TracesUnsentCommitment(cairo_obj.traces)
        self.composition = TableUnsentCommitment(cairo_obj.composition)
        self.oods_values = self.init_oods_values(cairo_obj.oods_values, 10)
        self.fri = FriUnsentCommitment(cairo_obj.fri)
        self.proof_of_work = ProofOfWorkUnsentCommitment(cairo_obj.proof_of_work)

    # n_oods_values := air.mask_size + air.constraint_degree.
    def init_oods_values(self, cairo_obj, n_oods_values) -> list[ChannelUnsentFelt]:
        res = []
        for i in range(n_oods_values):
            res.append(ChannelUnsentFelt(cairo_obj[i]))
        return res


class StarkCommitment:
    def __init__(self, cairo_obj) -> None:
        self.traces = TracesCommitment(cairo_obj.traces)
        self.composition = TableCommitment(cairo_obj.composition)
        self.interaction_after_composition = InteractionValuesAfterComposition(
            cairo_obj.interaction_after_composition
        )
        self.oods_values = self.init_oods_values(cairo_obj.oods_values)
        self.interaction_after_oods = InteractionValuesAfterOods(
            cairo_obj.interaction_after_oods
        )
        self.fri = FriCommitment(cairo_obj.fri)

    # n_oods_values := air.mask_size + air.constraint_degree.
    def init_oods_values(self, cairo_obj, n_oods_values) -> list[ChannelSentFelt]:
        res = []
        for i in range(n_oods_values):
            res.append(ChannelSentFelt(cairo_obj[i]))
        return res


class InteractionValuesAfterComposition:
    def __init__(self, cairo_obj) -> None:
        self.oods_point = Felt(cairo_obj.oods_point)


class InteractionValuesAfterOods:
    def __init__(self, cairo_obj) -> None:
        self.coefficients = FeltArray(cairo_obj.coefficients)


class StarkWitness:
    def __init__(self, cairo_obj) -> None:
        self.traces_decommitment = TracesDecommitment(cairo_obj.traces_decommitment)
        self.traces_witness = TracesWitness(cairo_obj.traces_witness)
        self.composition_decommitment = TableDecommitment(
            cairo_obj.composition_decommitment
        )
        self.composition_witness = TableCommitmentWitness(cairo_obj.composition_witness)
        self.fri_witness = FriWitness(cairo_obj.fri_witness)


class StarkWitness:
    def __init__(self, cairo_obj) -> None:
        self.config = StarkConfig(cairo_obj.config)
        self.public_input = PublicInput(cairo_obj.public_input)
        self.unsent_commitment = StarkUnsentCommitment(cairo_obj.unsent_commitment)
        self.witness = StarkUnsentCommitment(cairo_obj.witness)


class StarkConfig:
    def __init__(self, cairo_obj) -> None:
        self.traces = TracesConfig(cairo_obj.traces)
        self.composition = TableCommitmentConfig(cairo_obj.composition)
        self.fri = FriConfig(cairo_obj.fri)
        self.proof_of_work = ProofOfWorkConfig(cairo_obj.proof_of_work)
        self.log_trace_domain_size = Felt(cairo_obj.log_trace_domain_size)
        self.n_queries = Felt(cairo_obj.n_queries)
        self.log_n_cosets = Felt(cairo_obj.log_n_cosets)
        self.n_verifier_friendly_commitment_layers = Felt(
            cairo_obj.n_verifier_friendly_commitment_layers
        )


class TracesUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.original = TableUnsentCommitment(cairo_obj.original)
        self.interaction = TableUnsentCommitment(cairo_obj.interaction)


class TracesCommitment:
    def __init__(self, cairo_obj) -> None:
        self.public_input = PublicInput(cairo_obj.public_input)
        self.original = TableCommitment(cairo_obj.original)
        self.interaction_elements = FeltArray(cairo_obj.interaction_elements)
        self.interaction = TableCommitment(cairo_obj.interaction)


class TracesDecommitment:
    def __init__(self, cairo_obj) -> None:
        self.original = TableDecommitment(cairo_obj.original)
        self.interaction = TableDecommitment(cairo_obj.interaction)


class TracesWitness:
    def __init__(self, cairo_obj) -> None:
        self.original = TableCommitmentWitness(cairo_obj.original)
        self.interaction = TableCommitmentWitness(cairo_obj.interaction)


class TracesConfig:
    def __init__(self, cairo_obj) -> None:
        self.original = TableCommitmentConfig(cairo_obj.original)
        self.interaction = TableCommitmentConfig(cairo_obj.interaction)


class TableUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.vector = VectorUnsentCommitment(cairo_obj.vector)


class TableCommitment:
    def __init__(self, cairo_obj) -> None:
        self.config = TableCommitmentConfig(cairo_obj.config)
        self.vector_commitment = VectorCommitment(cairo_obj.vector_commitment)


class TableCommitmentConfig:
    def __init__(self, cairo_obj) -> None:
        self.conn_columnsfig = Felt(cairo_obj.n_columns)
        self.vector = VectorCommitmentConfig(cairo_obj.vector)


class TableDecommitment:
    def __init__(self, cairo_obj) -> None:
        self.n_values = Felt(cairo_obj.n_values)
        self.values = FeltArray(cairo_obj.values, self.n_values)


class TableCommitmentWitness:
    def __init__(self, cairo_obj) -> None:
        self.vector = VectorCommitmentWitness(cairo_obj.vector)


class VectorUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.commitment_hash = Felt(cairo_obj.commitment_hash)


class VectorCommitment:
    def __init__(self, cairo_obj) -> None:
        self.config = VectorCommitmentConfig(cairo_obj.config)
        self.commitment_hash = Felt(cairo_obj.commitment_hash)


class VectorCommitmentConfig:
    def __init__(self, cairo_obj) -> None:
        self.height = Felt(cairo_obj.height)
        self.n_verifier_friendly_commitment_layers = Felt(
            cairo_obj.n_verifier_friendly_commitment_layers
        )


class VectorCommitmentWitness:
    def __init__(self, cairo_obj) -> None:
        self.n_authentications = Felt(cairo_obj.n_authentications)
        self.authentications = FeltArray(
            cairo_obj.authentications, self.n_authentications
        )


class VectorQuery:
    def __init__(self, cairo_obj) -> None:
        self.index = Felt(cairo_obj.index)
        self.value = Felt(cairo_obj.value)


class VectorQueryWithDepth:
    def __init__(self, cairo_obj) -> None:
        self.index = Felt(cairo_obj.index)
        self.value = Felt(cairo_obj.value)
        self.depth = Felt(cairo_obj.depth)


class ProofOfWorkConfig:
    def __init__(self, cairo_obj) -> None:
        self.n_bits = Felt(cairo_obj.n_bits)


class ProofOfWorkUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.nonce = Felt(cairo_obj.nonce)


class StarkDomains:
    def __init__(self, cairo_obj) -> None:
        self.log_eval_domain_size = Felt(cairo_obj.log_eval_domain_size)
        self.eval_domain_size = Felt(cairo_obj.eval_domain_size)
        self.eval_generator = Felt(cairo_obj.eval_generator)
        self.log_trace_domain_size = Felt(cairo_obj.log_trace_domain_size)
        self.trace_domain_size = Felt(cairo_obj.trace_domain_size)
        self.trace_generator = Felt(cairo_obj.trace_generator)


class FriUnsentCommitment:
    def __init__(self, cairo_obj, n_layers, log_last_layer_degree_bound) -> None:
        self.inner_layers = TableUnsentCommitment(cairo_obj.inner_layers, n_layers - 1)
        self.last_layer_coefficients = FeltArray(
            cairo_obj.last_layer_coefficients, 2**log_last_layer_degree_bound
        )

    def init_inner_layers(self, cairo_obj, len) -> list[TableUnsentCommitment]:
        res = []
        for i in range(len):
            res.append(TableUnsentCommitment(cairo_obj[i]))
        return res

    def init_last_layer_coefficients(self, cairo_obj, len) -> list[ChannelUnsentFelt]:
        res = []
        for i in range(len):
            res.append(ChannelUnsentFelt(cairo_obj[i]))
        return res


class FriCommitment:
    def __init__(self, cairo_obj) -> None:
        self.config = FriConfig(cairo_obj.config)
        self.inner_layers = self.init_inner_layers(
            cairo_obj.inner_layers, self.config.n_layers - 1
        )
        self.eval_points = FeltArray(cairo_obj.eval_points, self.config.n_layers)
        self.last_layer_coefficients = self.init_last_layer_coefficients(
            cairo_obj.last_layer_coefficients,
            2**self.config.log_last_layer_degree_bound,
        )

    def init_inner_layers(self, cairo_obj, len) -> list[TableCommitment]:
        res = []
        for i in range(len):
            res.append(TableCommitment(cairo_obj[i]))
        return res

    def init_last_layer_coefficients(self, cairo_obj, len) -> list[ChannelSentFelt]:
        res = []
        for i in range(len):
            res.append(ChannelSentFelt(cairo_obj[i]))
        return res


class FriDecommitment:
    def __init__(self, cairo_obj) -> None:
        self.n_values = Felt(cairo_obj.n_values)
        self.values = FeltArray(cairo_obj.values, self.n_values)
        self.points = FeltArray(cairo_obj.points, self.n_values)


class FriLayerWitness:
    def __init__(self, cairo_obj) -> None:
        self.n_leaves = Felt(cairo_obj.n_leaves)
        self.leaves = FeltArray(cairo_obj.leaves, self.n_leaves)
        self.table_witness = TableCommitmentWitness(cairo_obj.table_witness)


class FriWitness:
    def __init__(self, cairo_obj, n_layers) -> None:
        self.layers = self.init_layers(cairo_obj.layers, n_layers - 1)

    def init_layers(self, cairo_obj, len) -> list[FriLayerWitness]:
        res = []
        for i in range(len):
            res.append(FriLayerWitness(cairo_obj[i]))
        return res


class FriConfig:
    def __init__(self, cairo_obj) -> None:
        self.log_input_size = Felt(cairo_obj.log_input_size)
        self.n_layers = Felt(cairo_obj.n_layers)
        self.inner_layers = self.init_inner_layers(
            cairo_obj.inner_layers, self.n_layers - 1
        )
        self.fri_step_sizes = FeltArray(cairo_obj.fri_step_sizes, self.n_layers)
        self.log_last_layer_degree_bound = Felt(cairo_obj.log_last_layer_degree_bound)

    def init_inner_layers(self, cairo_obj, len) -> list[TableCommitmentConfig]:
        res = []
        for i in range(len):
            res.append(TableCommitmentConfig(cairo_obj[i]))
        return res


class PublicInput:
    def __init__(self, cairo_obj) -> None:
        self.log_n_steps = Felt(cairo_obj.log_n_steps)
        self.range_check_min = Felt(cairo_obj.range_check_min)
        self.range_check_max = Felt(cairo_obj.range_check_max)
        self.layout = Felt(cairo_obj.layout)
        self.dynamic_params = FeltArray(cairo_obj.dynamic_params)
        self.n_segments = Felt(cairo_obj.n_segments)
        self.segments = SegmentInfo(cairo_obj.segments)
        self.padding_addr = Felt(cairo_obj.padding_addr)
        self.padding_value = Felt(cairo_obj.padding_value)
        self.main_page_len = Felt(cairo_obj.main_page_len)
        self.main_page = self.init_main_page(cairo_obj.main_page, self.main_page_len)
        self.n_continuous_pages = Felt(cairo_obj.n_continuous_pages)
        self.continuous_page_headers = self.init_continuous_page_headers(
            cairo_obj.continuous_page_headers, self.main_page_len
        )

    def init_main_page(self, cairo_obj, len) -> list[AddrValue]:
        res = []
        for i in range(len):
            res.append(AddrValue(cairo_obj[i]))
        return res

    def init_continuous_page_headers(
        self, cairo_obj, len
    ) -> list[ContinuousPageHeader]:
        res = []
        for i in range(len):
            res.append(ContinuousPageHeader(cairo_obj[i]))
        return res
