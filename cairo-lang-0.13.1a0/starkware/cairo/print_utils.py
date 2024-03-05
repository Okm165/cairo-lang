import json


class Felt:
    def __init__(self, cairo_obj) -> None:
        self.value = int(cairo_obj)

    def __repr__(self) -> str:
        return f"{hex(self.value)}"


class FeltArray:
    def __init__(self, memory, cairo_ptr, len) -> None:
        self.value = [Felt(memory[cairo_ptr + i]) for i in range(len)]

    def __repr__(self) -> str:
        return f"{self.value}"


class SegmentInfo:
    def __init__(self, cairo_obj) -> None:
        self.begin_addr = Felt(cairo_obj.begin_addr)
        self.stop_ptr = Felt(cairo_obj.stop_ptr)

    def __repr__(self) -> str:
        dict = {
            "begin_addr": self.begin_addr,
            "stop_ptr": self.stop_ptr,
        }
        return f"{dict}"


class AddrValue:
    def __init__(self, cairo_obj) -> None:
        self.address = Felt(cairo_obj.address)
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "address": self.address,
            "value": self.value,
        }
        return f"{dict}"


class ContinuousPageHeader:
    def __init__(self, cairo_obj) -> None:
        self.start_address = Felt(cairo_obj.start_address)
        self.size = Felt(cairo_obj.size)
        self.hash = Felt(cairo_obj.hash)
        self.prod = Felt(cairo_obj.prod)

    def __repr__(self) -> str:
        dict = {
            "start_address": self.start_address,
            "size": self.size,
            "hash": self.hash,
            "prod": self.prod,
        }
        return f"{dict}"


class ChannelUnsentFelt:
    def __init__(self, cairo_obj) -> None:
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "value": self.value,
        }
        return f"{dict}"


class ChannelSentFelt:
    def __init__(self, cairo_obj) -> None:
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "value": self.value,
        }
        return f"{dict}"


class StarkUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.traces = TracesUnsentCommitment(cairo_obj.traces)
        self.composition = TableUnsentCommitment(cairo_obj.composition)
        self.oods_values = self.init_oods_values(cairo_obj.oods_values, 10)
        self.fri = FriUnsentCommitment(cairo_obj.fri)
        self.proof_of_work = ProofOfWorkUnsentCommitment(cairo_obj.proof_of_work)

    def __repr__(self) -> str:
        dict = {
            "traces": self.traces,
            "composition": self.composition,
            "oods_values": self.oods_values,
            "fri": self.fri,
            "proof_of_work": self.proof_of_work,
        }
        return f"{dict}"

    # n_oods_values := air.mask_size + air.constraint_degree.
    def init_oods_values(self, cairo_obj, n_oods_values) -> list[ChannelUnsentFelt]:
        res = []
        for i in range(n_oods_values):
            res.append(ChannelUnsentFelt(cairo_obj[i]))
        return res


class StarkCommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.traces = TracesCommitment(memory, cairo_obj.traces)
        self.composition = TableCommitment(cairo_obj.composition)
        self.interaction_after_composition = InteractionValuesAfterComposition(
            cairo_obj.interaction_after_composition
        )
        self.oods_values = self.init_oods_values(cairo_obj.oods_values)
        self.interaction_after_oods = InteractionValuesAfterOods(
            cairo_obj.interaction_after_oods
        )
        self.fri = FriCommitment(cairo_obj.fri)

    def __repr__(self) -> str:
        dict = {
            "traces": self.traces,
            "composition": self.composition,
            "interaction_after_composition": self.interaction_after_composition,
            "oods_values": self.oods_values,
            "interaction_after_oods": self.interaction_after_oods,
            "fri": self.fri,
        }
        return f"{dict}"

    # n_oods_values := air.mask_size + air.constraint_degree.
    def init_oods_values(self, cairo_obj, n_oods_values) -> list[ChannelSentFelt]:
        res = []
        for i in range(n_oods_values):
            res.append(ChannelSentFelt(cairo_obj[i]))
        return res


class InteractionValuesAfterComposition:
    def __init__(self, cairo_obj) -> None:
        self.oods_point = Felt(cairo_obj.oods_point)

    def __repr__(self) -> str:
        dict = {
            "oods_point": self.oods_point,
        }
        return f"{dict}"


class InteractionValuesAfterOods:
    def __init__(self, memory, cairo_obj, n_oods_values) -> None:
        self.coefficients = FeltArray(memory, cairo_obj.coefficients, n_oods_values)

    def __repr__(self) -> str:
        dict = {
            "coefficients": self.coefficients,
        }
        return f"{dict}"


class StarkWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.traces_decommitment = TracesDecommitment(
            memory, cairo_obj.traces_decommitment
        )
        self.traces_witness = TracesWitness(cairo_obj.traces_witness)
        self.composition_decommitment = TableDecommitment(
            cairo_obj.composition_decommitment
        )
        self.composition_witness = TableCommitmentWitness(cairo_obj.composition_witness)
        self.fri_witness = FriWitness(cairo_obj.fri_witness)

    def __repr__(self) -> str:
        dict = {
            "traces_decommitment": self.traces_decommitment,
            "traces_witness": self.traces_witness,
            "composition_decommitment": self.composition_decommitment,
            "composition_witness": self.composition_witness,
            "fri_witness": self.fri_witness,
        }
        return f"{dict}"


class StarkWitness:
    def __init__(self, cairo_obj) -> None:
        self.config = StarkConfig(cairo_obj.config)
        self.public_input = PublicInput(cairo_obj.public_input)
        self.unsent_commitment = StarkUnsentCommitment(cairo_obj.unsent_commitment)
        self.witness = StarkUnsentCommitment(cairo_obj.witness)

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
            "public_input": self.public_input,
            "unsent_commitment": self.unsent_commitment,
            "witness": self.witness,
        }
        return f"{dict}"


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

    def __repr__(self) -> str:
        dict = {
            "traces": self.traces,
            "composition": self.composition,
            "fri": self.fri,
            "proof_of_work": self.proof_of_work,
            "log_trace_domain_size": self.log_trace_domain_size,
            "n_queries": self.n_queries,
            "log_n_cosets": self.log_n_cosets,
            "n_verifier_friendly_commitment_layers": self.n_verifier_friendly_commitment_layers,
        }
        return f"{dict}"


class TracesUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.original = TableUnsentCommitment(cairo_obj.original)
        self.interaction = TableUnsentCommitment(cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesCommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.public_input = PublicInput(memory, cairo_obj.public_input)
        self.original = TableCommitment(cairo_obj.original)
        self.interaction_elements = FeltArray(memory, cairo_obj.interaction_elements, 6)
        self.interaction = TableCommitment(cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "public_input": self.public_input,
            "original": self.original,
            "interaction_elements": self.interaction_elements,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesDecommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.original = TableDecommitment(memory, cairo_obj.original)
        self.interaction = TableDecommitment(memory, cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.original = TableCommitmentWitness(memory, cairo_obj.original)
        self.interaction = TableCommitmentWitness(memory, cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TracesConfig:
    def __init__(self, cairo_obj) -> None:
        self.original = TableCommitmentConfig(cairo_obj.original)
        self.interaction = TableCommitmentConfig(cairo_obj.interaction)

    def __repr__(self) -> str:
        dict = {
            "original": self.original,
            "interaction": self.interaction,
        }
        return f"{dict}"


class TableUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.vector = VectorUnsentCommitment(cairo_obj.vector)

    def __repr__(self) -> str:
        dict = {
            "vector": self.vector,
        }
        return f"{dict}"


class TableCommitment:
    def __init__(self, cairo_obj) -> None:
        self.config = TableCommitmentConfig(cairo_obj.config)
        self.vector_commitment = VectorCommitment(cairo_obj.vector_commitment)

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
            "vector_commitment": self.vector_commitment,
        }
        return f"{dict}"


class TableCommitmentConfig:
    def __init__(self, cairo_obj) -> None:
        self.n_columns = Felt(cairo_obj.n_columns)
        self.vector = VectorCommitmentConfig(cairo_obj.vector)

    def __repr__(self) -> str:
        dict = {
            "n_columns": self.n_columns,
            "vector": self.vector,
        }
        return f"{dict}"


class TableDecommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_values = Felt(cairo_obj.n_values)
        self.values = FeltArray(memory, cairo_obj.values, self.n_values.value)

    def __repr__(self) -> str:
        dict = {
            "n_values": self.n_values,
            "values": self.values,
        }
        return f"{dict}"


class TableCommitmentWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.vector = VectorCommitmentWitness(memory, cairo_obj.vector)

    def __repr__(self) -> str:
        dict = {
            "vector": self.vector,
        }
        return f"{dict}"


class VectorUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.commitment_hash = ChannelSentFelt(cairo_obj.commitment_hash)

    def __repr__(self) -> str:
        dict = {
            "commitment_hash": self.commitment_hash,
        }
        return f"{dict}"


class VectorCommitment:
    def __init__(self, cairo_obj) -> None:
        self.config = VectorCommitmentConfig(cairo_obj.config)
        self.commitment_hash = ChannelSentFelt(cairo_obj.commitment_hash)

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
        }
        return f"{dict}"


class VectorCommitmentConfig:
    def __init__(self, cairo_obj) -> None:
        self.height = Felt(cairo_obj.height)
        self.n_verifier_friendly_commitment_layers = Felt(
            cairo_obj.n_verifier_friendly_commitment_layers
        )

    def __repr__(self) -> str:
        dict = {
            "height": self.height,
            "n_verifier_friendly_commitment_layers": self.n_verifier_friendly_commitment_layers,
        }
        return f"{dict}"


class VectorCommitmentWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_authentications = Felt(cairo_obj.n_authentications)
        self.authentications = FeltArray(
            memory, cairo_obj.authentications, self.n_authentications.value
        )

    def __repr__(self) -> str:
        dict = {
            "n_authentications": self.n_authentications,
            "authentications": self.authentications,
        }
        return f"{dict}"


class VectorQuery:
    def __init__(self, cairo_obj) -> None:
        self.index = Felt(cairo_obj.index)
        self.value = Felt(cairo_obj.value)

    def __repr__(self) -> str:
        dict = {
            "index": self.index,
            "value": self.value,
        }
        return f"{dict}"


class VectorQueryWithDepth:
    def __init__(self, cairo_obj) -> None:
        self.index = Felt(cairo_obj.index)
        self.value = Felt(cairo_obj.value)
        self.depth = Felt(cairo_obj.depth)

    def __repr__(self) -> str:
        dict = {
            "index": self.index,
            "value": self.value,
            "depth": self.depth,
        }
        return f"{dict}"


class ProofOfWorkConfig:
    def __init__(self, cairo_obj) -> None:
        self.n_bits = Felt(cairo_obj.n_bits)

    def __repr__(self) -> str:
        dict = {
            "n_bits": self.n_bits,
        }
        return f"{dict}"


class ProofOfWorkUnsentCommitment:
    def __init__(self, cairo_obj) -> None:
        self.nonce = ChannelUnsentFelt(cairo_obj.nonce)

    def __repr__(self) -> str:
        dict = {
            "nonce": self.nonce,
        }
        return f"{dict}"


class StarkDomains:
    def __init__(self, cairo_obj) -> None:
        self.log_eval_domain_size = Felt(cairo_obj.log_eval_domain_size)
        self.eval_domain_size = Felt(cairo_obj.eval_domain_size)
        self.eval_generator = Felt(cairo_obj.eval_generator)
        self.log_trace_domain_size = Felt(cairo_obj.log_trace_domain_size)
        self.trace_domain_size = Felt(cairo_obj.trace_domain_size)
        self.trace_generator = Felt(cairo_obj.trace_generator)

    def __repr__(self) -> str:
        dict = {
            "log_eval_domain_size": self.log_eval_domain_size,
            "eval_domain_size": self.eval_domain_size,
            "eval_generator": self.eval_generator,
            "log_trace_domain_size": self.log_trace_domain_size,
            "trace_domain_size": self.trace_domain_size,
            "trace_generator": self.trace_generator,
        }
        return f"{dict}"


class FriUnsentCommitment:
    def __init__(self, cairo_obj, n_layers, log_last_layer_degree_bound) -> None:
        self.inner_layers = TableUnsentCommitment(cairo_obj.inner_layers, n_layers - 1)
        self.last_layer_coefficients = FeltArray(
            cairo_obj.last_layer_coefficients, 2**log_last_layer_degree_bound
        )

    def __repr__(self) -> str:
        dict = {
            "inner_layers": self.inner_layers,
            "last_layer_coefficients": self.last_layer_coefficients,
        }
        return f"{dict}"

    def init_inner_layers(self, cairo_obj, len) -> list[TableUnsentCommitment]:
        return [TableUnsentCommitment(cairo_obj[i]) for i in range(len)]

    def init_last_layer_coefficients(self, cairo_obj, len) -> list[ChannelUnsentFelt]:
        return [ChannelUnsentFelt(cairo_obj[i]) for i in range(len)]


class FriCommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.config = FriConfig(memory, cairo_obj.config)
        # self.inner_layers = self.init_inner_layers(
        #     cairo_obj.inner_layers, self.config.n_layers.value - 1
        # )
        self.eval_points = FeltArray(
            memory, cairo_obj.eval_points, self.config.n_layers.value
        )
        self.last_layer_coefficients = self.init_last_layer_coefficients(
            cairo_obj.last_layer_coefficients,
            2**self.config.log_last_layer_degree_bound.value,
        )

    def __repr__(self) -> str:
        dict = {
            "config": self.config,
            # "inner_layers": self.inner_layers,
            "eval_points": self.eval_points,
            "last_layer_coefficients": self.last_layer_coefficients,
        }
        return f"{dict}"

    def init_inner_layers(self, cairo_obj, len) -> list[TableCommitment]:
        return [TableCommitment(cairo_obj[i]) for i in range(len)]

    def init_last_layer_coefficients(self, cairo_obj, len) -> list[ChannelSentFelt]:
        return [ChannelSentFelt(cairo_obj[i]) for i in range(len)]


class FriDecommitment:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_values = Felt(cairo_obj.n_values)
        self.values = FeltArray(memory, cairo_obj.values, self.n_values.value)
        self.points = FeltArray(memory, cairo_obj.points, self.n_values.value)

    def __repr__(self) -> str:
        dict = {
            "n_values": self.n_values,
            "values": self.values,
            "points": self.points,
        }
        return f"{dict}"


class FriLayerWitness:
    def __init__(self, memory, cairo_obj) -> None:
        self.n_leaves = Felt(cairo_obj.n_leaves)
        self.leaves = FeltArray(memory, cairo_obj.leaves, self.n_leaves.value)
        self.table_witness = TableCommitmentWitness(memory, cairo_obj.table_witness)

    def __repr__(self) -> str:
        dict = {
            "n_leaves": self.n_leaves,
            "leaves": self.leaves,
            "table_witness": self.table_witness,
        }
        return f"{dict}"


class FriWitness:
    def __init__(self, memory, cairo_obj, n_layers) -> None:
        self.layers = self.init_layers(memory, cairo_obj.layers, n_layers.value - 1)

    def __repr__(self) -> str:
        dict = {
            "layers": self.layers,
        }
        return f"{dict}"

    def init_layers(self, memory, cairo_obj, len) -> list[FriLayerWitness]:
        return [FriLayerWitness(memory, cairo_obj[i]) for i in range(len)]


class FriConfig:
    def __init__(self, memory, cairo_obj) -> None:
        self.log_input_size = Felt(cairo_obj.log_input_size)
        self.n_layers = Felt(cairo_obj.n_layers)
        self.inner_layers = self.init_inner_layers(
            cairo_obj.inner_layers, self.n_layers.value - 1
        )
        self.fri_step_sizes = FeltArray(
            memory, cairo_obj.fri_step_sizes, self.n_layers.value
        )
        self.log_last_layer_degree_bound = Felt(cairo_obj.log_last_layer_degree_bound)

    def __repr__(self) -> str:
        dict = {
            "log_input_size": self.log_input_size,
            "n_layers": self.n_layers,
            "inner_layers": self.inner_layers,
            "fri_step_sizes": self.fri_step_sizes,
            "log_last_layer_degree_bound": self.log_last_layer_degree_bound,
        }
        return f"{dict}"

    def init_inner_layers(self, cairo_obj, len) -> list[TableCommitmentConfig]:
        return [TableCommitmentConfig(cairo_obj[i]) for i in range(len)]


class PublicInput:
    def __init__(self, memory, cairo_obj) -> None:
        self.log_n_steps = Felt(cairo_obj.log_n_steps)
        self.range_check_min = Felt(cairo_obj.range_check_min)
        self.range_check_max = Felt(cairo_obj.range_check_max)
        self.layout = Felt(cairo_obj.layout)
        self.dynamic_params = FeltArray(memory, cairo_obj.dynamic_params, 0)
        self.n_segments = Felt(cairo_obj.n_segments)
        self.segments = self.init_segments(cairo_obj.segments, self.n_segments.value)
        self.padding_addr = Felt(cairo_obj.padding_addr)
        self.padding_value = Felt(cairo_obj.padding_value)
        self.main_page_len = Felt(cairo_obj.main_page_len)
        self.main_page = self.init_main_page(
            cairo_obj.main_page, self.main_page_len.value
        )
        self.n_continuous_pages = Felt(cairo_obj.n_continuous_pages)
        self.continuous_page_headers = self.init_continuous_page_headers(
            cairo_obj.continuous_page_headers, self.n_continuous_pages.value
        )

    def __repr__(self) -> str:
        dict = {
            "log_n_steps": self.log_n_steps,
            "range_check_min": self.range_check_min,
            "range_check_max": self.range_check_max,
            "layout": self.layout,
            "dynamic_params": self.dynamic_params,
            "n_segments": self.n_segments,
            "segments": self.segments,
            "padding_addr": self.padding_addr,
            "padding_value": self.padding_value,
            "main_page_len": self.main_page_len,
            "main_page": self.main_page,
            "n_continuous_pages": self.n_continuous_pages,
            "continuous_page_headers": self.continuous_page_headers,
        }
        return f"{dict}"

    def init_segments(self, cairo_obj, len) -> list[SegmentInfo]:
        return [SegmentInfo(cairo_obj[i]) for i in range(len)]

    def init_main_page(self, cairo_obj, len) -> list[AddrValue]:
        return [AddrValue(cairo_obj[i]) for i in range(len)]

    def init_continuous_page_headers(
        self, cairo_obj, len
    ) -> list[ContinuousPageHeader]:
        return [ContinuousPageHeader(cairo_obj[i]) for i in range(len)]
